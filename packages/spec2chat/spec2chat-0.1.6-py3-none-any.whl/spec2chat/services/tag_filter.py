"""
spec2chat - A Python library for building task-oriented conversational systems from OpenAPI service specifications.

Author: M. Jesús Rodríguez
License: Apache 2.0 License
Version: 0.1.6
Repository: https://github.com/mjesusrodriguez/spec2chat
Created on 17/05/2025 by M. Jesús Rodríguez
"""

import openai
import spacy
from bson import ObjectId
from nltk.corpus import wordnet
from spec2chat.db.mongo import MongoDB
from spec2chat.utils.openai_config import configure_openai
from .service_selection import select_service_by_intent, service_selection
from itertools import chain

configure_openai()
db = MongoDB()

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise OSError(
        "SpaCy model 'en_core_web_sm' is not installed.\n"
        "Run:\n\n    python -m spacy download en_core_web_sm"
    )

def get_tags_from_service(service_id, domain):
    tags = []
    services = db.get_collection(domain, 'services')
    # Busco el servicio por id
    document = services.find_one({"_id": ObjectId(service_id)})

    # Check if the document exists and contains 'tags'
    if document and 'tags' in document:
        # Initialize example values
        tags = document['tags'][0]['name'].split(', ')

    #quito los tags repetidos
    unique_tags = list(set(tags))

    return unique_tags

def filter_services_by_tag(intent_services, user_tags, domain):
    # tagServices = []
    services = {}
    services_bbdd = db.get_collection(domain, 'services')

    for service_id in intent_services:
        # Busco el servicio por id
        document = services_bbdd.find_one({"_id": ObjectId(service_id)})

        # Encuentro el servicio (debería siempre darlo ya que lo hemos guardado previamente)
        if document:
            # Itero el JSON y saco los intents que tiene definido el servicio
            for tag_document in document.get('tags', []):
                tags = tag_document.get("name", "")

                # divido en tokens
                tagList = {substring.strip() for substring in tags.split(',')}

                # Por cada etiqueta del servicio que esté en las etiquetas del usuario
                for tag in user_tags:
                    if tag.lower() in tagList:
                        services[service_id] = services.get(service_id, 0) + 1

            # No hemos registrado ninguna etiqueta para ese servicio así que 0
            if service_id not in services:
                services[service_id] = 0

    # Ordena el diccionario por sus valores en orden ascendente
    sorted_services = dict(sorted(services.items(), key=lambda item: item[1]))
    return sorted_services

def get_synonyms(word):
    return list(set(lemma.name() for syn in wordnet.synsets(word) for lemma in syn.lemmas()))

def extract_tags(text):
    doc = nlp(text.lower())
    raw_tags = [token.text for token in doc if token.pos_ in ('ADJ', 'NOUN')]
    synonyms = list(set(chain.from_iterable(get_synonyms(tag) for tag in raw_tags)))
    return list(set(raw_tags + synonyms))

def generate_tag_question(tag, domain):

    messages = [{
        "role": "user",
        "content": f"Provide an informal yes/no question to understand a user's preference "
                   f"regarding the tag '{tag}' when selecting a {domain}."
    }]
    # Crear la solicitud de ChatCompletion
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Puedes usar "gpt-4" si tienes acceso
        messages=messages,
        temperature=0.3,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )
    # Extraer la respuesta generada por el modelo
    generated_text = response.choices[0].message.content
    return generated_text

def generate_tag_questions(tags, domain):
    return {tag: generate_tag_question(tag, domain) for tag in tags}

def get_additional_questions(services, user_input, intent, data_from_client, domain):
    filled_params = data_from_client["filledslots"]
    service_tags = set()
    service_tags_dict = {}

    for i, service_id in enumerate(services):
        tags = get_tags_from_service(service_id, domain)
        if i == 0:
            service_tags = set(tags)
        else:
            service_tags = service_tags.symmetric_difference(tags)
        service_tags_dict[service_id] = service_tags

    aditional_questions = generate_tag_questions(service_tags, domain)

    for tag in service_tags:
        filled_params[tag] = ""

    return aditional_questions, filled_params

def tag_filter(user_input, intent, data_from_client, domain):
    user_tags = extract_tags(user_input)

    # Elimino items repetidos
    unique_tags = list(set(user_tags))

    intent_services = select_service_by_intent(intent, domain)

    tag_services = filter_services_by_tag(intent_services, unique_tags, domain)
    selected_services = service_selection(tag_services, user_input, data_from_client["filledslots"], intent, domain)
    return selected_services

def detect_positive_answers(response_dict):
    positive_keywords = ["yes", "yeah", "yep", "sure", "absolutely", "definitely", "of course"]
    return [tag for tag, answer in response_dict.items() if any(k in answer.lower() for k in positive_keywords)]