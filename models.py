from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base


class IDRecord(Base):
    __tablename__ = "id_records"

    id = Column(Integer, primary_key=True, index=True)
    prn = Column(String, index=True)
    confidence = Column(Float)
    image_path = Column(String)          # ID card image
    prn_image_path = Column(String)      # Cropped PRN image
    result_json_path = Column(String)    # OCR / detection metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
