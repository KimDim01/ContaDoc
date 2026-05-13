import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "ContaDoc AI Enterprise"
    # Hugging Face Config
    HF_API_TOKEN: str = os.getenv("HF_API_TOKEN", "")
    HF_BASE_URL: str = "https://router.huggingface.co/v1"
    # Default Model - you can change this to any model available on HF Router
    HF_MODEL: str = "meta-llama/Llama-3.1-70B-Instruct"

    VECTOR_DB_PATH: str = "data/vector_db"
    UPLOAD_DIR: str = "data/uploads"

settings = Settings()
