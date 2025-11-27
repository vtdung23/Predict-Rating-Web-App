"""
Configuration Settings
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database
DATABASE_URL = "sqlite:///./app/database/rating_prediction.db"

# Security
SECRET_KEY = "your-secret-key-change-in-production-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Uploads
UPLOAD_DIR = BASE_DIR / "app" / "static" / "uploads"
WORDCLOUD_DIR = UPLOAD_DIR / "wordclouds"

# Create directories if they don't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
WORDCLOUD_DIR.mkdir(parents=True, exist_ok=True)

# Products (simulated dataset)
PRODUCTS = [
    "Điện thoại iPhone 15 Pro Max",
    "Laptop Dell XPS 13",
    "Tai nghe Sony WH-1000XM5",
    "Máy ảnh Canon EOS R5",
    "Đồng hồ thông minh Apple Watch Series 9",
    "Tivi Samsung QLED 65 inch",
    "Máy lạnh Daikin Inverter",
    "Tủ lạnh LG InstaView",
]
