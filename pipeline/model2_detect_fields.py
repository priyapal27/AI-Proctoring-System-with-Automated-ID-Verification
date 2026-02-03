import cv2
import os
from inference_sdk import InferenceHTTPClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=os.getenv("ROBOFLOW_API_KEY")
)

MODEL_ID = "prn_photo_detection/1"   # your trained model‑2

def crop_prn(id_card_path, output_dir="outputs/fields"):
    os.makedirs(output_dir, exist_ok=True)

    img = cv2.imread(id_card_path)
    result = CLIENT.infer(id_card_path, model_id=MODEL_ID)

    for pred in result["predictions"]:
        if pred["class"] == "prn":
            x1 = int(pred["x"] - pred["width"] / 2)
            y1 = int(pred["y"] - pred["height"] / 2)
            x2 = int(pred["x"] + pred["width"] / 2)
            y2 = int(pred["y"] + pred["height"] / 2)

            crop = img[y1:y2, x1:x2]
            out_path = os.path.join(output_dir, "prn.jpg")
            cv2.imwrite(out_path, crop)

            return out_path

    return None
