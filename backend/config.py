# config.py
import os

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///herboai.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    ALLOWED_IMAGE_EXT = os.getenv("ALLOWED_IMAGE_EXT", "jpg,jpeg,png,webp")
    CORS_ORIGINS = [x.strip() for x in os.getenv("CORS_ORIGINS","http://localhost:3000").split(",")]
