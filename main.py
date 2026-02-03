from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pipeline.pipeline import run_pipeline
from database import SessionLocal
from models import IDRecord
from datetime import datetime
from pathlib import Path
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins (safe for local dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

BASE_DIR = Path(__file__).resolve().parent
BASE_OUTPUT = BASE_DIR / "outputs"

(BASE_OUTPUT / "id_cards").mkdir(parents=True, exist_ok=True)
(BASE_OUTPUT / "fields").mkdir(parents=True, exist_ok=True)
(BASE_OUTPUT / "results").mkdir(parents=True, exist_ok=True)


@app.post("/detect-id")
async def detect_id(file: UploadFile = File(...)):
    image_path = os.path.join(UPLOAD_DIR, file.filename)

    # 1️⃣ Save uploaded image
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2️⃣ Run pipeline (THIS CREATES temp outputs)
    result = run_pipeline(image_path)

    prn = result.get("prn")
    confidence = result.get("confidence")

    # ❌ Exit early if PRN not found
    if not prn:
        return {
            "status": "fail",
            "verified": False,
            "data": None,
            "message": "ID number not detected"
        }

    # 3️⃣ TEMP model output paths (DEFINE FIRST)
    TEMP_ID_CARD = BASE_DIR / "outputs" / "id_cards" / "id_card.jpg"
    TEMP_PRN_IMG = BASE_DIR / "outputs" / "fields" / "prn.jpg"
    TEMP_JSON = BASE_DIR / "outputs" / "results" / "results.json"

    # 🔍 Debug (NOW variables exist)
    print("TEMP ID:", TEMP_ID_CARD, os.path.exists(TEMP_ID_CARD))
    print("TEMP PRN:", TEMP_PRN_IMG, os.path.exists(TEMP_PRN_IMG))
    print("TEMP JSON:", TEMP_JSON, os.path.exists(TEMP_JSON))

    # 4️⃣ Generate unique prefix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = f"{timestamp}_{prn}"

    # 5️⃣ FINAL unique output paths
    FINAL_ID_CARD = BASE_OUTPUT / "id_cards" / f"{prefix}.jpg"
    FINAL_PRN_IMG = BASE_OUTPUT / "fields" / f"{prefix}_prn.jpg"
    FINAL_JSON = BASE_OUTPUT / "results" / f"{prefix}.json"

    # 6️⃣ Copy (archive) files
    if TEMP_ID_CARD.exists():
        shutil.copy(TEMP_ID_CARD, FINAL_ID_CARD)

    if TEMP_PRN_IMG.exists():
        shutil.copy(TEMP_PRN_IMG, FINAL_PRN_IMG)

    if TEMP_JSON.exists():
        shutil.copy(TEMP_JSON, FINAL_JSON)

    # 7️⃣ Save to DB
    db = SessionLocal()
    try:
        record = IDRecord(
            prn=prn,
            confidence=confidence,
            image_path=str(FINAL_ID_CARD),
            prn_image_path=str(FINAL_PRN_IMG),
            result_json_path=str(FINAL_JSON)
        )
        db.add(record)
        db.commit()
    finally:
        db.close()

    return {
        "status": "success",
        "verified": True,
        "data": {
            "prn": prn,
            "confidence": confidence
        }
    }


