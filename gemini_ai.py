import google.generativeai as genai
from config import Config

def ask_gemini_with_prompt(prompt: str) -> str:
    """Envía el prompt a Gemini y devuelve el texto de respuesta."""
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
    resp = model.generate_content(prompt)
    return getattr(resp, "text", "") or ""
