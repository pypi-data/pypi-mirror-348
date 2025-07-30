"""
spec2chat - A Python library for building task-oriented conversational systems from OpenAPI service specifications.

Author: M. Jesús Rodríguez
License: Apache 2.0 License
Version: 0.1.6
Repository: https://github.com/mjesusrodriguez/spec2chat
Created on 17/05/2025 by M. Jesús Rodríguez
"""

import json
from spec2chat.services.domain_manager import classify_domain
from spec2chat.services.intent_recognition import recognize_intent
from spec2chat.services.slot_filling import extract_slots, slot_filling
from spec2chat.services.service_selection import (
    select_service_by_intent,
    service_selection
)
from spec2chat.services.question_generation import generate_question_for_slot
from spec2chat.services.question_improvement import improve_question
from spec2chat.services.open_domain import open_domain_conversation
from spec2chat.services.slot_ranking import get_top_parameters_combined
from spec2chat.services.tag_filter import (
    tag_filter,
    get_additional_questions,
)
from spec2chat.services.question_retrieval import get_service_questions as retrieve_service_questions
def filter_services_with_tags(user_input: str, intent: str, data_from_client: dict, domain: str):
    return tag_filter(user_input, intent, data_from_client, domain)

def generate_additional_tag_questions(services: list, user_input: str, intent: str, data_from_client: dict, domain: str):
    return get_additional_questions(services, user_input, intent, data_from_client, domain)

def get_top_discriminative_parameters(domain: str) -> list:
    return get_top_parameters_combined(domain)

def continue_open_domain_conversation(user_input: str, dialogue_history: list = None) -> str:
    return open_domain_conversation(user_input, dialogue_history)

def analyze_input(user_input: str) -> list:
    return classify_domain(user_input)

def detect_intent(user_input: str, domain: str) -> str:
    return recognize_intent(user_input, domain)

def extract_required_slots(intent: str, service_id: str, domain: str) -> list:
    """Devuelve la lista de parámetros requeridos para un intent concreto en un servicio OpenAPI."""
    return extract_slots(intent, service_id, domain)

def complete_slot_filling(user_input: str, domain: str, intent: str, service_id: str, user_answers=None) -> dict:
    """Rellena los valores de los parámetros detectados en el input."""
    slots = extract_slots(intent, service_id, domain)
    filled = slot_filling(user_input, slots, user_answers)
    return {
        "input": user_input,
        "domain": domain,
        "intent": intent,
        "slots": json.loads(filled)
    }

def get_services_for_intent(intent: str, domain: str) -> list:
    """Recupera los servicios cuyo intent coincide con el solicitado."""
    return select_service_by_intent(intent, domain)

def disambiguate_services(tag_services: dict, user_input: str, slots: dict, intent: str, domain: str) -> list:
    """Desambigua entre servicios empatados usando los slots del usuario."""
    return service_selection(tag_services, user_input, slots, intent, domain)

def generate_question(slot: str, domain: str) -> str:
    return generate_question_for_slot(slot, domain)

def improve_slot_question(question: str, domain: str) -> str:
    return improve_question(question, domain)

def extract_filled_slots(user_input: str, slots: list, user_answers=None) -> dict:
    filled = slot_filling(user_input, slots, user_answers)
    print("[DEBUG] Raw filled (str):", filled)

    try:
        parsed = json.loads(filled)
        print("[DEBUG] Parsed filled (dict):", parsed)
        return parsed
    except json.JSONDecodeError as e:
        print("[ERROR] Could not parse filled JSON:", e)
        return {}

def get_service_questions(service_id: str, intent: str, domain: str) -> dict:
    """
    Recupera las preguntas específicas del servicio para rellenar slots.
    """
    return retrieve_service_questions(service_id, intent, domain)

def slot_filling_direct(user_input: str, slots: list, user_answers=None) -> str:
    """
    Llama directamente al sistema de slot filling y devuelve el resultado en formato JSON string.
    (Versión directa sin conversión a dict).
    """
    return slot_filling(user_input, slots, user_answers)