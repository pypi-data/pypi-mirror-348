"""
spec2chat - A Python library for building task-oriented conversational systems from OpenAPI service specifications.

Author: M. Jesús Rodríguez
License: Apache 2.0 License
Version: 0.1.6
Repository: https://github.com/mjesusrodriguez/spec2chat
Created on 17/05/2025 by M. Jesús Rodríguez
"""

from spec2chat.core.manager import (
    analyze_input as retrieve_domains,
    detect_intent as retrieve_intent,
    get_top_discriminative_parameters,
    complete_slot_filling,
    generate_question,
    improve_slot_question,
    extract_required_slots as extractSlots,
    filter_services_with_tags,
    generate_additional_tag_questions,
    get_services_for_intent as select_service_by_intent,
    disambiguate_services as select_services_by_tags,
    get_service_questions,
    slot_filling_direct
)

import random
from bson import ObjectId
import re
import json

from spec2chat.services.question_improvement import improve_question
from spec2chat.services.tag_filter import detect_positive_answers

GOODBYE_KEYWORDS = [
    'goodbye', 'bye', 'see you', 'later', 'farewell', 'take care',
    'thanks', 'thank you', 'talk to you later', 'bye bye'
]

OPEN_DOMAIN_PHRASES = [
    r'what do you think', r'tell me about', r'can you share',
    r'what is your opinion', r'explain to me'
]

def check_for_goodbye(user_input: str) -> bool:
    return any(re.search(rf'\b{kw}\b', user_input.lower()) for kw in GOODBYE_KEYWORDS)

def detect_open_domain(user_input: str) -> bool:
    return any(re.search(pattern, user_input.lower()) for pattern in OPEN_DOMAIN_PHRASES)


def run_chatbot(
    user_input: str,
    user_answers: list = None,
    tasks: dict = None,
    domain: str = '',
    intent: str = '',
    service_id: str = '',
    services: list = None,
    filledslots: dict = None,
    reqslots: list = None
) -> dict:
    """
    Ejecuta el flujo completo del chatbot de forma autocontenida.
    """

    user_answers = user_answers or []
    tasks = tasks or {}
    services = services or []
    filledslots = filledslots or {}
    reqslots = reqslots or []

    # Fase 0: Detección de diálogo abierto
    if detect_open_domain(user_input):
        return {
            'chatbot_answer': 'I’m happy to chat! What would you like to talk about?',
            'dom': 'out-of-domain',
            'useranswers': user_answers + [{
                "user": user_input,
                "chatbot": "I’m happy to chat! What would you like to talk about?"
            }]
        }

    # Fase 1: Detección de dominios
    if not domain:
        detected_domains = retrieve_domains(user_input)
        if isinstance(detected_domains, str):
            detected_domains = [detected_domains]
        domain = detected_domains[0] if detected_domains else ''
    else:
        detected_domains = [domain]

    # Fase 2: Detección de intenciones
    if not tasks:
        for d in detected_domains:
            tasks[d] = retrieve_intent(user_input, d)

    intent = intent or tasks.get(domain, '')
    intent = intent.lower() if intent else ''

    # Fase 3: Delegar en función completa del flujo
    return manage_task_oriented_dialogue(
        user_input=user_input,
        user_answers=user_answers,
        tasks=tasks,
        service_id=service_id,
        services=services,
        filledslots=filledslots,
        reqslots=reqslots,
        domain=domain,
        intent=intent
    )


def complete_slot_filling(user_input, user_answers, filledslots, reqslots, service_id, intent, domain, tasks):
    """
    Realiza el slot filling final y genera preguntas para los parámetros que falten.
    """
    expected_slots = extractSlots(intent, service_id, domain)
    new_filled = slot_filling_direct(user_input, expected_slots, user_answers)

    # 🔧 Añadir este bloque para manejar el caso de lista de diccionarios
    if isinstance(new_filled, str):
        try:
            new_filled = json.loads(new_filled)
        except json.JSONDecodeError:
            print("[ERROR] No se pudo parsear la respuesta JSON")
            new_filled = {}

    if isinstance(new_filled, list):
        try:
            new_filled = {list(d.keys())[0]: list(d.values())[0] for d in new_filled}
        except Exception as e:
            print("[ERROR] Al convertir lista a diccionario:", e)
            new_filled = {}

    emptyParams = {}
    for k, v in new_filled.items():
        if isinstance(v, str):
            if v.lower() != "null":
                filledslots[k] = v
            else:
                emptyParams[k] = None
        elif v is not None:
            filledslots[k] = v
        else:
            emptyParams[k] = None

    # Eliminar los que ya se preguntaron antes
    for param in reqslots:
        emptyParams.pop(param, None)

    service_questions = get_service_questions(service_id, intent, domain).get("questions", {})
    questions = {}

    for param in emptyParams:
        if param in service_questions:
            improved = improve_slot_question(service_questions[param], domain)
            if improved:
                questions[param] = improved

    response = {
        'questions': questions,
        'filledslots': filledslots,
        'service_id': str(service_id),
        'intent': intent,
        'dom': domain,
        'tasks': tasks,
        'final': True,
        'reqslots': reqslots
    }

    # Si no hay preguntas y ya se ha marcado como final, terminamos la conversación
    if response.get("final") is True and (not questions or all(v == '' for v in questions.values())):
        print("[DEBUG] Finalizado: todos los slots completados y no hay preguntas pendientes.")
        response["end_of_conversation"] = True

    return response

def parse_slot_response(raw_response):
    """
    Convierte la respuesta del modelo a un diccionario plano {slot: value},
    independientemente del formato (dict, JSON string, lista de dicts).
    """
    if isinstance(raw_response, dict):
        return raw_response

    if isinstance(raw_response, str):
        try:
            loaded = json.loads(raw_response)
            # Aquí está la parte crítica
            if isinstance(loaded, list):
                merged = {}
                for item in loaded:
                    if isinstance(item, dict):
                        merged.update(item)
                return merged
            elif isinstance(loaded, dict):
                return loaded
            else:
                print("[ERROR] JSON string no es ni lista ni dict")
                return {}
        except json.JSONDecodeError as e:
            print("[ERROR] Could not decode JSON:", e)
            return {}

    if isinstance(raw_response, list):
        merged = {}
        for item in raw_response:
            if isinstance(item, dict):
                merged.update(item)
        return merged

    return {}

def clean_question_text(q):
    return re.sub(r'^[\'"]|[\'"]$', '', q.strip())

def manage_task_oriented_dialogue(
    user_input: str,
    user_answers: list,
    tasks: dict,
    service_id: str = '',
    services: list = None,
    filledslots: dict = None,
    reqslots: list = None,
    domain: str = '',
    intent: str = ''
) -> dict:
    """
    Maneja el flujo de diálogo orientado a tareas como función interna autocontenida.
    """

    if not filledslots:
        filledslots = {}

    if not domain:
        domain = list(tasks.keys())[0]
        intent = tasks[domain]
    else:
        intent = intent or tasks.get(domain)

    # Slot filling inicial si filledslots aún está vacío
    if not any(filledslots.values()):
        top_params = get_top_discriminative_parameters(domain)
        top_slots = [p['parameter'] for p in top_params]

        extracted = slot_filling_direct(user_input, top_slots, user_answers)
        extracted = parse_slot_response(extracted)

        print("[DEBUG ORCH] RAW EXTRACTED:", extracted)
        print("[DEBUG ORCH] EXTRACTED TYPE:", type(extracted))
        print("[DEBUG ORCH] ITEMS TO ADD:", {k: v for k, v in extracted.items() if v and v.lower() != "null"})

        filledslots.update({k: v for k, v in extracted.items() if v and v.lower() != "null"})

        print("[DEBUG ORCH] FILLING INICIAL completado:", filledslots)

    # Si ya tenemos el servicio identificado, hacemos el slot filling final
    if service_id:
        return complete_slot_filling(
            user_input, user_answers, filledslots, reqslots,
            service_id, intent, domain, tasks
        )

    # Si hay múltiples servicios candidatos
    if services:
        if reqslots and len(filledslots) > len(reqslots):
            # Ya se han respondido preguntas adicionales -> slot filling final
            # Seleccionar el mejor servicio basado en slots
            tag_services = filter_services_with_tags(user_input, intent, {
                "filledslots": filledslots,
                "useranswers": user_answers
            }, domain)

            selected_services = tag_services.get("services") if isinstance(tag_services, dict) else tag_services
            if not selected_services:
                return {'chatbot_answer': 'Lo siento, no se encontró un servicio adecuado.',
                        'end_of_conversation': True}

            selected = selected_services[0]  # o aplicar alguna lógica más elaborada

            return complete_slot_filling(
                user_input, user_answers, filledslots, reqslots,
                service_id=selected, intent=intent, domain=domain, tasks=tasks
            )

    # Si aún no tenemos servicios pero sí parámetros suficientes -> filtramos
    top_params = get_top_discriminative_parameters(domain)
    top_slots = [p['parameter'] for p in top_params]
    if all(filledslots.get(p, '') != '' for p in top_slots):
        tag_services = filter_services_with_tags(user_input, intent, {
            "filledslots": filledslots,
            "useranswers": user_answers
        }, domain)

        selected_services = tag_services.get("services") if isinstance(tag_services, dict) else tag_services

        if len(selected_services) == 1:
            return complete_slot_filling(
                user_input, user_answers, filledslots, reqslots=top_slots,
                service_id=selected_services[0], intent=intent, domain=domain, tasks=tasks
            )

        elif len(selected_services) > 1:
            questions, updated_slots = generate_additional_tag_questions(
                selected_services, user_input, intent,
                {"filledslots": filledslots}, domain
            )
            return {
                'questions': questions,
                'filledslots': updated_slots,
                'intent': intent,
                'userinput': user_input,
                'services': [str(s) for s in selected_services],
                'dom': domain,
                'reqslots': top_slots,
                'tasks': tasks
            }

    # Si aún faltan slots por rellenar, preguntamos por ellos
    pending_questions = {}
    for slot in top_slots:
        if slot not in filledslots or filledslots[slot] in ('', None, "null"):
            pending_questions[slot] = generate_question(slot, domain)

    if pending_questions:
        return {
            'questions': pending_questions,
            'filledslots': filledslots,
            'intent': intent,
            'userinput': user_input,
            'services': [],
            'dom': domain,
            'reqslots': top_slots,
            'tasks': tasks
        }

    # Si no hay nada que preguntar ni servicios seleccionables, devolvemos error
    return {
        'chatbot_answer': 'Lo siento, no pude encontrar un servicio adecuado.',
        'end_of_conversation': True
    }
