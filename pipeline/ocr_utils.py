import easyocr
import re

reader = easyocr.Reader(['en'])

def extract_prn(image_path):
    results = reader.readtext(image_path)

    for bbox, text, conf in results:
        text = text.replace(" ", "")
        if conf > 0.6 and re.fullmatch(r"\d{10,15}", text):
            return text, float(conf)

    return None, 0.0

