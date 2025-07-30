"""
Ejemplo básico de uso de la librería spec2chat.

Este script muestra cómo iniciar una conversación con el chatbot
a partir de una entrada del usuario. La función principal expuesta por la librería
es `run_chatbot()`, la cual orquesta todo el flujo conversacional.

Antes de ejecutar, asegúrate de:
  - Tener una base de datos MongoDB activa con los servicios cargados
  - Haber definido la variable de entorno OPENAI_API_KEY
  - Tener instalados los modelos necesarios:
        python -m nltk.downloader wordnet
        python -m spacy download en_core_web_sm
"""

from spec2chat.core.orchestrator import run_chatbot

# Entrada del usuario simulando el inicio de una conversación
user_input = "I'm looking for a cheap vegetarian restaurant"

# Lista de respuestas anteriores (puede estar vacía en el primer turno)
user_answers = []

# Ejecutar la conversación (punto de entrada principal de la librería)
response = run_chatbot(user_input, user_answers=user_answers)

# Mostrar resultado
print("\n===== RESPUESTA DEL CHATBOT =====\n")
print(response)

"""
Salida esperada (ejemplo):
---------------------------
El chatbot devuelve un diccionario con la información necesaria para continuar la conversación.
Este diccionario puede incluir:

- 'questions': diccionario {slot -> pregunta} para seguir recogiendo datos
- 'filledslots': slots que ya se han rellenado automáticamente
- 'intent': intención detectada
- 'dom': dominio detectado
- 'tasks': diccionario con el resto de tareas pendientes
- 'service_id': si ya hay un servicio seleccionado
- 'final': True si ya estamos en la última etapa del diálogo

Ejemplo de salida:

{
    'questions': {
        'pricerange': 'How much are you willing to spend?',
        'food': 'What type of food do you prefer?'
    },
    'filledslots': {
        'food': 'vegetarian'
    },
    'intent': 'bookrestaurant',
    'userinput': "I'm looking for a cheap vegetarian restaurant",
    'dom': 'restaurant',
    'reqslots': ['pricerange', 'food'],
    'tasks': {'restaurant': 'bookrestaurant'}
}

Puedes usar este diccionario para mostrar preguntas al usuario, almacenar la conversación, o integrarlo en un frontend.
"""