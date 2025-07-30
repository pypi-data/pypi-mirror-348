"""
spec2chat - A Python library for building task-oriented conversational systems from OpenAPI service specifications.

Author: M. Jesús Rodríguez
License: Apache 2.0 License
Version: 0.1.6
Repository: https://github.com/mjesusrodriguez/spec2chat
Created on 17/05/2025 by M. Jesús Rodríguez
"""

import openai
from spec2chat.utils.openai_config import configure_openai

configure_openai()

def generate_question_for_slot(slot: str, domain: str) -> str:
    """Genera una pregunta coloquial para un slot específico en un dominio, sin saludo inicial."""

    messages = [
        {
            "role": "user",
            "content": (
                f"You are a task-oriented chatbot specialized in the '{domain}' domain. "
                f"Create a colloquial question to request the value of this slot: '{slot}'. "
                f"Do not include greetings or salutations."
            )
        }
    ]

    # Crear la solicitud de ChatCompletion
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Puedes usar "gpt-4" si tienes acceso
        messages=messages,
        temperature=0,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    generated_text = response.choices[0].message.content
    cleaned = generated_text.replace('"', '').replace("'", "")
    return cleaned