# imageinsightai/captioner.py

from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

class ImageCaptioner:
    def __init__(self):
        print("Loading model... This may take a few seconds.")
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    def describe(self, image_path: str) -> str:
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(image, return_tensors="pt")
        output = self.model.generate(**inputs)
        caption = self.processor.decode(output[0], skip_special_tokens=True)
        return caption
