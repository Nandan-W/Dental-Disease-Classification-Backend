import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MODEL_PATH = os.getenv('MODEL_PATH', 'model/best_model.keras')
    
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}