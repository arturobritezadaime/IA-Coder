import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Clase de configuración del proyecto."""
    FRED_API_KEY = os.getenv("FRED_API_KEY")
    NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")
    GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    EMAIL = os.getenv("EMAIL")
    FREEPIK_API_KEY = os.getenv("FREEPIK_API_KEY")
    HEADERS_SEC = {"User-Agent": EMAIL}