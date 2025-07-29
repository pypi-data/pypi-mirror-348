#
# https://github.com/JoHof/lungmask
#
# Downloading: "https://github.com/JoHof/lungmask/releases/download/v0.0/unet_r231-d5d2fc3d.pth" to /home/test/.cache/torch/hub/checkpoints/unet_r231-d5d2fc3d.pth
# Downloading: "https://github.com/JoHof/lungmask/releases/download/v0.0/unet_ltrclobes-3a07043d.pth" to /home/test/.cache/torch/hub/checkpoints/unet_ltrclobes-3a07043d.pth
# Downloading: "https://github.com/JoHof/lungmask/releases/download/v0.0/unet_r231covid-0de78a7e.pth" to /home/test/.cache/torch/hub/checkpoints/unet_r231covid-0de78a7e.pth
#
import os
import datetime
import requests
import SimpleITK as sitk
from lungmask import LMInferer

# You may find more lung data at https://nbia.cancerimagingarchive.net/nbia-search/
DEFAULT_TESTDATA_URL = "https://github.com/JoHof/lungmask/raw/refs/heads/master/tests/testdata/0.dcm"

models = [
    "R231",
    "LTRCLobes",
    "R231CovidWeb",
]

def download_example(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        local_path = f"./tmp-{(datetime.datetime.now()).strftime('%Y-%m-%d-%H-%M-%S')}.dcm"
        with open(local_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Example downloaded and saved to file: {local_path}")
        return local_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")

input_dcm_file = download_example(DEFAULT_TESTDATA_URL)

img_in = sitk.ReadImage(input_dcm_file)
os.remove(input_dcm_file) # after DCM image read, remove downloaded tmp example file

for idx, model_name in enumerate(models):
    print(f"{idx}. {model_name}")
model_idx = int(input("Type model number and press Enter: "))

### BEGIN Remote part if Deeplogix RPC module used
inferer = LMInferer(modelname=models[model_idx]) # create LMInferer instance
labels = inferer.apply(img_in) # inference here
### END Remote part if Deeplogix RPC module used

img_label = sitk.GetImageFromArray(labels) # turn nympy.ndarray to SimpleITK.Image
img_label.CopyInformation(img_in) # Copies the Origin, Spacing, and Direction from the source image

img_in_pp = sitk.RescaleIntensity(img_in, 0, 32767)
img_in_pp = sitk.Cast(img_in_pp, sitk.sitkUInt16)
img_in_pp = sitk.RescaleIntensity(img_in_pp, 0, 65534)

img_label_pp = sitk.Cast(img_label, sitk.sitkUInt8)

img_out = sitk.LabelOverlay(image=img_in_pp, labelImage=img_label_pp, opacity=0.3)
imin, imax = sitk.MinimumMaximum(img_in_pp)
img_out = sitk.RescaleIntensity(img_out, imin, imax)

in_fname = f"./lungmask-input-{(datetime.datetime.now()).strftime('%Y-%m-%d-%H-%M-%S')}.png"
sitk.WriteImage(img_in_pp, in_fname)
print(f"Input lungmask sample: {in_fname}")

out_fname = f"./lungmask-result-{(datetime.datetime.now()).strftime('%Y-%m-%d-%H-%M-%S')}.png"
sitk.WriteImage(img_out, out_fname)
print(f"Lungmask result: {out_fname}")
