# Deeplogix AI RPC

Deeplogix AI RPC is a Python module for seamlessly running remote private AI models from your Python code as if these models were installed locally.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) for install.

Development version from TestPyPi:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple deeplogix
```

Production production version from PyPi:

```bash
pip install deeplogix
```

## Usage

For module built-in demos:

```bash
python -m deeplogix --demo
```

Or for your A.I. script:

```bash
python -m deeplogix --run ./my/script.py
```

Or just:

```bash
python -m deeplogix
```

And it will print usage options:
```
usage: python -m deeplogix [--demo] [--run ./my/script.py] [--dev] [--log {DEBUG,INFO,WARNING,ERROR}]

options:
  --demo                Run built-in demo.
  --run ./my/script.py  Run user's script.
  --dev                 Show exceptions in console. Default: each exception logged to separate file.
  --log {DEBUG,INFO,WARNING,ERROR}
                        Set the logging level. Default: INFO.
```

When you run Deeplogix module first time - it will ask you hostId and token, which could be obtained at [Deeplogix](https://www.deeplogix.io/) site after sign up.

## License

[MIT](https://choosealicense.com/licenses/mit/)
