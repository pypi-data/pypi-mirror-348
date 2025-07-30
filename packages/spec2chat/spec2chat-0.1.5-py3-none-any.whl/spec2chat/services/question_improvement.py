import openai
from spec2chat.utils.openai_config import configure_openai

configure_openai()

def improve_question(question: str, domain: str) -> str:
    """Reformula una pregunta para que sea más natural, educada y conversacional, manteniendo la intención."""

    messages = [
        {
            "role": "user",
            "content": (
                f"Given the original question: '{question}' in the context of the '{domain}' domain, "
                f"rephrase this question into a more conversational, polite, and natural tone. "
                f"Ensure the new question still elicits the same specific information from the customer. "
                f"Provide only one alternative question that maintains clarity and fits the domain’s context."
            )
        }
    ]

    # Crear la solicitud de ChatCompletion
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Puedes usar "gpt-4" si tienes acceso
        messages=messages,
        temperature=0.8,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    final_response = response.choices[0].message.content
    return final_response if final_response else question