import openai
from spec2chat.utils.openai_config import configure_openai

configure_openai()

def open_domain_conversation(user_input: str, dialogue_history: list = None) -> str:
    """
    Responde a una entrada de usuario en una conversación de dominio abierto.
    Usa el historial de diálogo si se proporciona.
    """

    dialogue_history_str = (
        "\n".join([f"User: {entry['user']}\nChatbot: {entry['chatbot']}" for entry in dialogue_history])
        if dialogue_history else ""
    )

    if dialogue_history_str:
        messages = [
            {
                "role": "system",
                "content": "You are an open-domain chatbot that engages in friendly, casual conversations with the user."
            },
            {
                "role": "user",
                "content": f"The current conversation is as follows:\n{dialogue_history_str}\nContinue the conversation with this input: {user_input}"
            }
        ]
    else:
        messages = [
            {
                "role": "system",
                "content": "You are an open-domain chatbot that engages in friendly, casual conversations with the user."
            },
            {
                "role": "user",
                "content": f"Start a conversation with this input: {user_input}"
            }
        ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=128,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    return response["choices"][0]["message"]["content"].strip()