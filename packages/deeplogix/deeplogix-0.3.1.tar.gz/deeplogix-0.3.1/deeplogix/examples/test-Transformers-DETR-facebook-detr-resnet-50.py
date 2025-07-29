# https://huggingface.co/facebook/detr-resnet-50
import datetime
import requests
import torch
from PIL import Image, ImageDraw, ImageFont
from transformers import DetrImageProcessor, DetrForObjectDetection

EXAMPLE_IMAGE_URL = "http://images.cocodataset.org/val2017/000000039769.jpg"

LOCAL_ID2LABEL = {
    "0": "N/A",    "1": "person",    "2": "bicycle",    "3": "car",    "4": "motorcycle",    "5": "airplane",
    "6": "bus",    "7": "train",    "8": "truck",    "9": "boat",    "10": "traffic light",    "11": "fire hydrant",
    "12": "N/A",    "13": "stop sign",    "14": "parking meter",    "15": "bench",    "16": "bird",    "17": "cat",
    "18": "dog",    "19": "horse",    "20": "sheep",    "21": "cow",    "22": "elephant",    "23": "bear",    "24": "zebra",
    "25": "giraffe",    "26": "N/A",    "27": "backpack",    "28": "umbrella",    "29": "N/A",    "30": "N/A",    "31": "handbag",
    "32": "tie",    "33": "suitcase",    "34": "frisbee",    "35": "skis",    "36": "snowboard",    "37": "sports ball",
    "38": "kite",    "39": "baseball bat",    "40": "baseball glove",    "41": "skateboard",    "42": "surfboard",    "43": "tennis racket",
    "44": "bottle",    "45": "N/A",    "46": "wine glass",    "47": "cup",    "48": "fork",    "49": "knife",    "50": "spoon",
    "51": "bowl",    "52": "banana",    "53": "apple",    "54": "sandwich",    "55": "orange",    "56": "broccoli",    "57": "carrot",
    "58": "hot dog",    "59": "pizza",    "60": "donut",    "61": "cake",    "62": "chair",    "63": "couch",    "64": "potted plant",
    "65": "bed",    "66": "N/A",    "67": "dining table",    "68": "N/A",    "69": "N/A",    "70": "toilet",    "71": "N/A",
    "72": "tv",    "73": "laptop",    "74": "mouse",    "75": "remote",    "76": "keyboard",    "77": "cell phone",    "78": "microwave",
    "79": "oven",    "80": "toaster",    "81": "sink",    "82": "refrigerator",    "83": "N/A",    "84": "book",    "85": "clock",
    "86": "vase",    "87": "scissors",    "88": "teddy bear",    "89": "hair drier",    "90": "toothbrush"
}

print(f"Downloading example input: {EXAMPLE_IMAGE_URL} ...")
image = Image.open(requests.get(EXAMPLE_IMAGE_URL, stream=True).raw)

### BEGIN Remote part if Deeplogix RPC module used
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)
results = processor.post_process_object_detection(outputs, target_sizes=torch.tensor([image.size[::-1]]), threshold=0.9)[0]
### END Remote part if Deeplogix RPC module used

# draw bboxes and export output image
draw = ImageDraw.Draw(image)

for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    # draw bbox
    x_min, y_min, x_max, y_max = [round(i, 2) for i in box.tolist()]
    draw.rectangle([(x_min, y_min), (x_max, y_max)], outline="green", width=2)
    # draw title
    title = LOCAL_ID2LABEL[f"{label.item()}"] # if model's config not exists locally, i.e. fully remote inference
    #title = model.config.id2label[label.item()] # if model's config exists locally
    font = ImageFont.load_default()
    text_width, text_height = [draw.textlength(title, font=font), 15]
    draw.rectangle([(x_min, y_min - text_height - 2), (x_min + text_width + 2, y_min)], fill="green")
    draw.text((x_min + 1, y_min - text_height - 1), title, fill="white", font=font)

image_fname = f"./detr-facebook-resnet-50-result-{(datetime.datetime.now()).strftime('%Y-%m-%d-%H-%M-%S')}.png"
image.save(image_fname)
print(f"Result saved to: {image_fname}")
