import cv2
import os
from datetime import datetime
print('Downloading model configuration...')
from ultralytics import YOLO
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

model_path = "best.pt"
yolo_model = YOLO(model_path)
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")
trocr_model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-printed")
def detect_and_ocr(image):
    results = yolo_model.predict(source=image, imgsz=640, conf=0.25)
    if len(results[0].boxes) == 0:
        return None

    box = results[0].boxes[0]
    x1, y1, x2, y2 = box.xyxy[0].tolist()
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

    if isinstance(image, str):
        img_cv = cv2.imread(image)
    else:
        img_cv = image
    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    cropped = img_cv[y1:y2, x1:x2]

    cropped_pil = Image.fromarray(cropped)
    pixel_values = processor(images=cropped_pil, return_tensors="pt").pixel_values
    generated_ids = trocr_model.generate(pixel_values)
    recognized_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

    return recognized_text

def process_image(image_path):
    frame = cv2.imread(image_path)
    if frame is None:
        raise ValueError(f"Cannot load image: {image_path}")

    recognized_text = detect_and_ocr(frame)
    timestamp = datetime.now()
    return recognized_text, timestamp, frame

def process_frame(frame):
    recognized_text = detect_and_ocr(frame)
    timestamp = datetime.now()
    return recognized_text, timestamp, frame
