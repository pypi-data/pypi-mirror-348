"""
spec2chat - A Python library for building task-oriented conversational systems from OpenAPI service specifications.

Author: M. Jesús Rodríguez
License: Apache 2.0 License
Version: 0.1.6
Repository: https://github.com/mjesusrodriguez/spec2chat
Created on 17/05/2025 by M. Jesús Rodríguez
"""

from spec2chat.db.mongo import MongoDB
from itertools import chain
import spacy

nlp = spacy.load("en_core_web_md")
db = MongoDB()

def get_top_parameters_combined(domain: str) -> list:
    """
    Devuelve los dos parámetros con mayor frecuencia combinada (servicio + usuario).
    """
    collection = db.get_collection(domain, "slot_ranking")
    all_parameters = collection.find()

    combined_parameters = []
    for param in all_parameters:
        combined_frequency = param.get("service_frequency", 0) + param.get("user_frequency", 0)
        combined_parameters.append({
            "parameter": param["parameter"],
            "combined_frequency": combined_frequency,
            "values": param.get("values", [])
        })

    combined_parameters.sort(key=lambda x: x["combined_frequency"], reverse=True)
    return combined_parameters[:2]

def update_frequencies_for_requested_slots(slots_list: list, req_slots: list, domain: str):
    """
    Actualiza la frecuencia de uso para los slots solicitados por el sistema si el usuario los ha mencionado.
    """
    collection = db.get_collection(domain, "slot_ranking")

    for slots_dict in slots_list:
        if isinstance(slots_dict, dict):
            for slot in req_slots:
                if slots_dict.get(slot) and slots_dict[slot].lower() != "null":
                    collection.update_one(
                        {"parameter": slot},
                        {"$inc": {"user_frequency": 1}},
                        upsert=True
                    )

def generate_ngrams(tokens, n):
    return zip(*[tokens[i:] for i in range(n)])

def detect_and_update_other_slots(user_input: str, top_slots_list: list, domain: str):
    """
    Detecta parámetros adicionales mencionados por el usuario y actualiza sus frecuencias.
    """
    collection = db.get_collection(domain, "slot_ranking")
    top_slots = set(slot['parameter'] for slot in top_slots_list)

    user_input_doc = nlp(user_input.lower())
    user_tokens = [token.text for token in user_input_doc]

    unigrams = user_tokens
    bigrams = [' '.join(gram) for gram in generate_ngrams(user_tokens, 2)]
    trigrams = [' '.join(gram) for gram in generate_ngrams(user_tokens, 3)]
    all_ngrams = list(chain(unigrams, bigrams, trigrams))

    for param in collection.find():
        param_name = param["parameter"]
        if param_name not in top_slots:
            for value in param.get("values", []):
                if value.lower() in all_ngrams:
                    collection.update_one(
                        {"parameter": param_name},
                        {"$inc": {"user_frequency": 1}},
                        upsert=True
                    )