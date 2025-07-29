import abc
import os.path
from os import listdir
from os.path import isfile, join
import sys
import runpy
import pickle
import json
import logging
import time
import datetime
import inspect
import uuid
import urllib.parse
import importlib.util
import subprocess
import signal
import traceback
import argparse

# global settings
WS_URI = "wss://dispatcher.deeplogix.io/?type=client&hostId={host_id}"
WAIT_RESULT_TIMEOUT = 600 # 10 min

# Clean exit on Ctrl+C
def on_sigint(sig, frame):
    print("\nCtrl+C pressed.\nBye.")
    os._exit(0)


signal.signal(signal.SIGINT, on_sigint)

# Parse CLI arguments
cli_parser = argparse.ArgumentParser(prog="python -m deeplogix", add_help=False)
cli_parser.add_argument("--demo", action="store_true", help="Run built-in demo.")
cli_parser.add_argument("--run", metavar="./my/script.py", help="Run user's script.")
cli_parser.add_argument("--dev", action="store_true", help="Show exceptions in console. Default: each exception logged to separate file.")
cli_parser.add_argument('--log', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO', help="Set the logging level. Default: INFO.")
cli_args = cli_parser.parse_known_args()[0]
if(not cli_args.demo and not cli_args.run):
    cli_parser.print_help()
    os._exit(0)

# Set log level
logging.basicConfig(encoding='utf-8', level=getattr(logging, cli_args.log))


# Print exception info
def print_exception(e):
    print(f"Exception Type: {type(e).__name__}\n")
    print(f"Exception Message: {e}\n")
    traceback.print_exc()


# Log exceptions to files
def log_exception(e):
    efname = f"exception-{(datetime.datetime.now()).strftime('%Y-%m-%d-%H-%M-%S')}.txt"
    with open(efname, "w") as file:
        file.write(f"Exception Type: {type(e).__name__}\n")
        file.write(f"Exception Message: {e}\n")
        traceback.print_exc(file=file)
        file.close()
    logging.error(f"Exception occured and was logged to file \"{efname}\", please send it to support@deeplogix.io")


# check and install additional packages if necessary
required_packages = [
    {"spec_name": "socketio", "install_name": "python-socketio"},
    {"spec_name": "websocket", "install_name": "websocket-client"},
    {"spec_name": "torch", "install_name": "torch"},
    {"spec_name": "transformers", "install_name": "transformers"},
    {"spec_name": "diffusers", "install_name": "diffusers"},
    {"spec_name": "lungmask", "install_name": "lungmask"},
]


def pip_check_install():
    packages_to_install = []
    for package in required_packages:
        if importlib.util.find_spec(package["spec_name"]) is None:
            packages_to_install.append(package["install_name"])
    if len(packages_to_install) > 0:
        print("Following packages are required (printing them in requirements.txt format) :")
        for name in packages_to_install:
            print(name)
        if ('y' != input(f"\nDo you want to install them (y/n)? ").lower()):
            print("Bye.")
            os._exit(1)
        cmd = [sys.executable, "-m", "pip", "install"] + packages_to_install
        print(" ".join(cmd))
        subprocess.check_call(cmd)


pip_check_install()

# following line requires `python-socketio` and `websocket-client`
import socketio

# globals
sio = socketio.Client()  # requires `import socketio` above
responses = {}
KEY_DEEPLOGIX_HOST_ID = 'deeplogix_host_id'
whitelist_restore = [
    'pipeline',
    'AutoModelForCausalLM',
    'AutoTokenizer',
    'DetrImageProcessor',
    'DetrForObjectDetection',
    'StableDiffusion3Pipeline',
    'FluxPipeline',
    'LMInferer'
]


# function for get current module base dir
def get_module_directory():
    current_frame = inspect.currentframe()
    if current_frame is not None and current_frame.f_back is not None:
        current_file = inspect.getfile(current_frame.f_back)
        return os.path.dirname(os.path.abspath(current_file))
    return None


# communications with backend
def get_request_id():
    return str(uuid.uuid4())


def set_response(req_id, res, host_id=None):
    if isinstance(res, list):
        res = res[0] if len(res) > 0 else {}
    if host_id is not None:
        res[KEY_DEEPLOGIX_HOST_ID] = host_id
    responses[req_id] = res


@sio.event
def connect():
    logging.debug("Successfully connected to dispatcher")


@sio.event
def disconnect():
    logging.debug("Disconnected from dispatcher")


@sio.event
def ready(is_ready):
    logging.debug("All events defined")
    if not is_ready:
        return
    # run client script
    try:
        if (cli_args.demo):
            # run built-in demos if --demo specified
            module_dir = get_module_directory()
            if module_dir:
                logging.debug(f"Module `deeplogix` directory is: {module_dir}")
            else:
                logging.error("Could not determine `deeplogix` module directory for run demos!")
                os._exit(1)
            examples_dir = module_dir + "/examples"
            print(f"Demos:")
            demo_files = [f for f in listdir(examples_dir) if isfile(join(examples_dir, f))]
            for demo_id, demo_fname in enumerate(demo_files):
                print(f"{demo_id}. {demo_fname}")
            selected_demo_idx = int(input("Type demo number and press Enter: "))
            script = f"{examples_dir}/{demo_files[selected_demo_idx]}"
            logging.debug(f"Starting: {script}")
            runpy.run_path(script, run_name="__main__")  # Execute demo script
            logging.debug(f"Script finished {script}")
        elif (cli_args.run):
            # run user's script
            logging.debug(f"Run script {cli_args.run}")
            runpy.run_path(cli_args.run, run_name="__main__")  # Execute the script
            logging.debug(f"Script finished {cli_args.run}")
        else:
            cli_parser.print_help()
    except Exception as e:
        print_exception(e) if cli_args.dev else log_exception(e)
    finally:
        sio.disconnect()


@sio.event
def result(res, req_id=None, host_id=None):
    if (None == req_id):
        logging.error(f"It seems Agent on the host is down, so Dispatcher can't find host for process the request.")
        os._exit(1)
    if isinstance(res, dict) and not res.get('result'):
        logging.debug(f"<<< {req_id=} {res=}")
        return set_response(req_id, res, host_id)
    response = pickle.loads(res)  # TODO: filter pickle.loads() to prevent RCE at client side?
    logging.debug(f"<<< {req_id=} {response=}")
    set_response(req_id, response, host_id)


@sio.event
def error(e):
    logging.error(f"Dispatcher error: {e}")
    if "E_HOST_ID_OR_TOKEN-IS_NOT_EXIST" == e:
        logging.error(f"Delete credentials.json file and restart, then enter correct hostId and token.")


def connect_to_dispatcher(token):
    try:
        if sio.connected:
            sio.disconnect()
        logging.debug("Connecting to dispatcher ...")
        sio.connect(
            WS_URI.format(host_id=''),
            transports=["websocket"],
            headers={
                'token': token
            })
        sio.wait()
    except socketio.exceptions.ConnectionError as e:
        logging.error("Error connecting to dispatcher!")
        print_exception(e) if cli_args.dev else log_exception(e)
        os._exit(1)


def restore_method(method, *args, **kwargs):
    method, call = method.split(".") if '.' in method else [method, '']
    if method not in whitelist_restore:
        logging.error(f"Method '{method}' is not whitelisted.")
        return
    _method = globals()[method]
    logging.debug(method)
    if bool(call):
        return getattr(_method, call)(*args, **kwargs)
    return _method(*args, **kwargs)


def sio_rpc_call(method, args, kwargs, instance=None):
    try:
        global WAIT_RESULT_TIMEOUT
        req_id = get_request_id()
        req = pickle.dumps({
            "method": method,
            "args": args,
            "kwargs": kwargs
        })
        logging.debug(f">>> {req_id=} {req=}")
        sio.emit("rpc", {
            "req_id": req_id,
            "req": req,
            "host_id": getattr(instance, KEY_DEEPLOGIX_HOST_ID, None) if instance is not None else None
        })
        logging.debug(f"Waiting RPC {method=} response ...")
        sec = 0
        while responses.get(req_id, None) is None:
            time.sleep(0.1)
            sec += 0.1
            if sec > WAIT_RESULT_TIMEOUT:
                raise ValueError("Timeout waiting for response")
        res = responses[req_id]
        if res.get(KEY_DEEPLOGIX_HOST_ID, None) is not None and instance:
            setattr(instance, KEY_DEEPLOGIX_HOST_ID, res.get(KEY_DEEPLOGIX_HOST_ID, None))
            res.pop(KEY_DEEPLOGIX_HOST_ID, None)
        responses.pop(req_id)
        logging.debug(f"<<< {req_id=} {res=}")
        if res['result']:
            return res # OK
        # Next lines are for Dispatcher or Agent errors handling, if result is false
        retval = res.get('retval', None)
        if retval is None:
            raise ValueError(f"The \"retval\" key is missing in Dipatcher response. {res}")
        error_message = res['retval'].get('msg', 'Unknown error at Dispatcher or Agent.')
        require_method = retval.get('require_method', None)
        if require_method is not None and instance is not None:
            # If Agent down and Dispatcher routed request to another Agent
            restored = restore_method(require_method, *instance.restore_args, **instance.restore_kwargs)
            if restored is None:
                raise ValueError(error_message)
            return sio_rpc_call(method, args, kwargs, instance)
        # Next lines are for Dispatcher only errors handling
        error_code = retval.get('code', None)
        match error_code:
            case 'E_AGENT-NOT_ACTIVE_RETRY':
                setattr(instance, KEY_DEEPLOGIX_HOST_ID, None)
                return sio_rpc_call(method, args, kwargs, instance)
            case 'E_INSUFFICIENT_FUNDS':
                print_exception(error_message) if cli_args.dev else log_exception(error_message)
                os._exit(1)
            case _:
                raise ValueError(error_message)
    except Exception as e:
        print_exception(e) if cli_args.dev else log_exception(e)


class DeeplogixManage:
    def __init__(self, res=None, *args, **kwargs):
        self.restore_args = args
        self.restore_kwargs = kwargs
        if res is None or (type(res) is dict and not res.get('result')):
            return
        setattr(self, KEY_DEEPLOGIX_HOST_ID, res.get(KEY_DEEPLOGIX_HOST_ID, None))


# https://huggingface.co/docs/transformers/v4.49.0/en/pipeline_tutorial
class Tokenizer(DeeplogixManage):

    def apply_chat_template(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs, self)
        return res["retval"]


class Pipeline(DeeplogixManage):
    def __init__(self, res=None, *args, **kwargs):
        super().__init__(res, *args, **kwargs)
        self.tokenizer = Tokenizer(res,*args, **kwargs)

    def __call__(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs, self)
        return res["retval"]


def pipeline(*args, **kwargs) -> Pipeline:
    res = sio_rpc_call(sys._getframe().f_code.co_name, args, kwargs)
    return Pipeline(res,*args, **kwargs)


# https://huggingface.co/docs/transformers/v4.49.0/en/model_doc/auto
class AutoModelForCausalLM(DeeplogixManage):

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        res = sio_rpc_call(f"{cls.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return cls(res,*args, **kwargs)

    def generate(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs, self)
        return res["retval"]


class AutoTokenizer(DeeplogixManage):
    def __call__(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs, self)
        return res["retval"]

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        res = sio_rpc_call(f"{cls.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return cls(res, *args, **kwargs)

    def decode(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs, self)
        return res["retval"]


# https://huggingface.co/facebook/detr-resnet-50
class DetrImageProcessor(DeeplogixManage):
    def __call__(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs, self)
        return res["retval"]

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        res = sio_rpc_call(f"{cls.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return cls(res, *args, **kwargs)

    def post_process_object_detection(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs, self)
        return res["retval"]


class DetrForObjectDetection(DeeplogixManage):
    def __call__(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs, self)
        return res["retval"]

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        res = sio_rpc_call(f"{cls.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return cls(res, *args, **kwargs)


# https://huggingface.co/docs/diffusers/main/en/api/pipelines/stable_diffusion/stable_diffusion_3
class StableDiffusion3Pipeline(DeeplogixManage):
    def __call__(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs, self)
        return res["retval"]

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        res = sio_rpc_call(f"{cls.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return cls(res, *args, **kwargs)


# https://huggingface.co/docs/diffusers/main/en/api/pipelines/flux
class FluxPipeline(DeeplogixManage):
    def __call__(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs, self)
        return res["retval"]

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        res = sio_rpc_call(f"{cls.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return cls(res, *args, **kwargs)


# https://github.com/JoHof/lungmask
class LMInferer(DeeplogixManage):
    def __init__(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        super().__init__(res, *args, **kwargs)

    def apply(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs, self)
        return res["retval"]


def main():
    # MonkeyPatch AI modiules with our overrides
    if importlib.util.find_spec("transformers") is not None:
        import transformers
        transformers.pipeline = pipeline
        transformers.AutoModelForCausalLM = AutoModelForCausalLM
        transformers.AutoTokenizer = AutoTokenizer
        transformers.DetrImageProcessor = DetrImageProcessor  # DETR, for example facebook/detr-resnet-50
        transformers.DetrForObjectDetection = DetrForObjectDetection  # DETR, for example facebook/detr-resnet-50
    if importlib.util.find_spec("diffusers") is not None:
        import diffusers
        diffusers.StableDiffusion3Pipeline = StableDiffusion3Pipeline
        diffusers.FluxPipeline = FluxPipeline
    if importlib.util.find_spec("lungmask") is not None:
        import lungmask
        lungmask.LMInferer = LMInferer
    # Check credentials for access Deeplogix features
    if not os.path.exists('./credentials.json'):
        token = input("Enter token: ")
        with open('./credentials.json', 'w+') as f:
            json.dump({'token': token}, f)
    else:
        with open('./credentials.json', 'r') as f:
            credentials = json.load(f)
            token = credentials['token']
    connect_to_dispatcher(token)


if __name__ == "__main__":
    logging.debug("DeepLogix module loaded!")
    try:
        main()
    except Exception as e:
        print_exception(e) if cli_args.dev else log_exception(e)
