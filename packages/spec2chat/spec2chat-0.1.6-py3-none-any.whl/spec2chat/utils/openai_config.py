import openai
import os

def configure_openai():
    """Set up OpenAI API key from environment variable."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "La variable de entorno OPENAI_API_KEY no está definida. "
            "Por favor, defínela antes de usar la librería."
        )
    openai.api_key = api_key