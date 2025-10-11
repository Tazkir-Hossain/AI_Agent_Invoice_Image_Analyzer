import os
from dotenv import load_dotenv
load_dotenv()
class Settings:
    APP_NAME: str = "Invoice Analyzer Agent"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama-3.1-70b-versatile")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
settings = Settings()
