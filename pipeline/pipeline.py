from .model1_crop_id import crop_id_card
from .model2_detect_fields import crop_prn
from .ocr_utils import extract_prn

def run_pipeline(input_image_path):
    id_card = crop_id_card(input_image_path)
    if not id_card:
        return {"error": "ID card not detected"}

    prn_crop = crop_prn(id_card)
    if not prn_crop:
        return {"error": "PRN not detected"}

    prn, confidence = extract_prn(prn_crop)

    if prn is None:
        return {
            "prn": None,
            "confidence": 0.0
        }

    return {
        "prn": prn,
        "confidence": confidence
    }

    
