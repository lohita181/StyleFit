import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Upload folders
    SECRET_KEY      = os.getenv('SECRET_KEY', 'dev-fallback-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOP_UPLOAD_FOLDER    = os.path.join(BASE_DIR, 'static', 'uploads', 'tops')
    BOTTOM_UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads', 'bottoms')

    # Model paths
    TOP_MODEL_PATH       = os.path.join(BASE_DIR, 'models', 'top_classifier.keras')
    BOTTOM_MODEL_PATH    = os.path.join(BASE_DIR, 'models', 'bottom_classifier.keras')
    TOP_LABELS_PATH      = os.path.join(BASE_DIR, 'models', 'top_labels.pkl')
    BOTTOM_LABELS_PATH   = os.path.join(BASE_DIR, 'models', 'bottom_labels.pkl')

    # Allowed file types
    ALLOWED_EXTENSIONS   = {'png', 'jpg', 'jpeg'}

    # Occasion mapping
    OCCASION_MAPPING = {
        "workout":             "sports wear",
        "adventure activities": "sports wear",
        "business meeting":    "office wear",
        "graduation ceremony": "office wear",
        "summer vacation":     "summer vacation",
        "birthday party":      "birthday party",
    }
    @staticmethod
    def user_upload_dir(user_id, clothing_type):
        path = os.path.join(BASE_DIR, 'static', 'uploads', str(user_id), clothing_type)
        os.makedirs(path, exist_ok=True)
        return path