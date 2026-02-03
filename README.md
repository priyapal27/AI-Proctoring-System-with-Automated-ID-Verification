# ID Detection & Verification Backend

A FastAPI-powered backend for automated ID card detection and PRN (Permanent Registration Number) extraction using a multi-stage computer vision pipeline.

## 🚀 Features

- **Automated ID Detection**: Automatically crops ID cards from full-sized images.
- **Field Extraction**: Locates and crops the PRN field using specialized models.
- **OCR Verification**: Extracts and validates PRN text using EasyOCR and regex.
- **Data Persistence**: Stores verification results and cropped assets in an SQLite database.
- **Asset Archiving**: Automatically versions and saves detections for audit trails.

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Computer Vision**: 
  - [Roboflow Inference SDK](https://roboflow.com) (Object Detection)
  - [EasyOCR](https://github.com/JaidedAI/EasyOCR) (Text Recognition)
  - OpenCV (Image processing)
- **Validation**: Regex & Confidence filtering

## 📋 Directory Structure

```text
backend/
├── main.py              # FastAPI application & endpoints
├── models.py            # Database schema (IDRecord)
├── database.py          # SQLAlchemy configuration
├── init_db.py           # Database initialization script
├── id_records.db        # SQLite database (auto-generated)
├── pipeline/            # Vision processing logic
│   ├── pipeline.py      # Main pipeline orchestrator
│   ├── model1_crop_id.py # ID card detection (Roboflow)
│   ├── model2_detect_fields.py # PRN field detection (Roboflow)
│   └── ocr_utils.py     # OCR & Text extraction (EasyOCR)
├── uploads/             # Temporary storage for uploaded images
└── outputs/             # Archived results (organized by type)
    ├── id_cards/
    ├── fields/
    └── results/
```

## 🏁 Getting Started

### Prerequisites

- Python 3.8+
- [Roboflow API Key](https://app.roboflow.com/) (Currently hardcoded in the pipeline files)

### Installation

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn sqlalchemy inference-sdk easyocr opencv-python
   ```
3. **Initialize the database**:
   ```bash
   python init_db.py
   ```

### Running the Application

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## 📡 API Usage

### Detect ID
**Endpoint**: `POST /detect-id`  
**Payload**: `file` (UploadFile)

**Example Request**:
```bash
curl -X POST "http://127.0.0.1:8000/detect-id" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@my_id.jpg"
```

**Success Response**:
```json
{
  "status": "success",
  "verified": true,
  "data": {
    "prn": "1234567890",
    "confidence": 0.85
  }
}
```

## 🧠 Pipeline Logic

The system uses a sequential "Waterfall" approach:
1. **Model 1**: Detects the ID card footprint and crops it.
2. **Model 2**: Finds the specific "PRN" field area within the cropped ID.
3. **EasyOCR**: Performs OCR on the field crop, applying regex to filter for numeric patterns (10-15 digits).
