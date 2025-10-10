# models.py
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from database import Base

class Plant(Base):
    __tablename__ = "plant"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)                 # default locale: en
    scientific_name = Column(String(150), nullable=False, unique=True)
    ayush_system = Column(String(50), nullable=False)          # Ayurveda/Unani/Siddha/Homeopathy/etc.
    category = Column(String(60))
    synonyms = Column(Text)                                    # CSV or JSON
    parts_used = Column(Text)                                  # JSON list
    uses = Column(Text)                                        # free text
    phytochemicals = Column(Text)
    dosage = Column(Text)                                      # “adults: …, children: …”
    contraindications = Column(Text)
    formulations = Column(Text)
    languages_json = Column(Text, nullable=False, default="{}")# {"en": {...}, "hi": {...}, "mr": {...}}
    description = Column(Text)
    properties = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    taste = Column(Text)
    dosha = Column(Text)
    therapeutic_uses = Column(Text)


    images = relationship("Image", back_populates="plant", cascade="all, delete-orphan")

class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey("plant.id"), nullable=False, index=True)
    file_path = Column(String(255), nullable=False, unique=True)
    alt_text = Column(String(255))
    plant = relationship("Plant", back_populates="images")

class Remedy(Base):
    __tablename__ = "remedy"
    id = Column(Integer, primary_key=True)
    symptom = Column(String(120), nullable=False)              # canonical label ("joint pain", "cough")
    diagnosis_pattern = Column(Text)                           # keywords/regex/notes
    plant_ids = Column(Text)                                   # "1,3,5"
    preparation = Column(Text)
    dosage = Column(Text)
    lifestyle_recommendations = Column(Text)
    preparation_method = Column(Text)
    ayush_system = Column(String(50))
    side_effects = Column(Text)
    contraindications = Column(Text)
    languages_json = Column(Text, nullable=False, default="{}")
    created_at = Column(DateTime, default=datetime.utcnow)

class AdminUser(Base):
    __tablename__ = "admin_user"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
