"""
spec2chat - A Python library for building task-oriented conversational systems from OpenAPI service specifications.

Author: M. Jesús Rodríguez
License: Apache 2.0 License
Version: 0.1.6
Repository: https://github.com/mjesusrodriguez/spec2chat
Created on 17/05/2025 by M. Jesús Rodríguez
"""

from bson import ObjectId
import random

from spec2chat.db.mongo import MongoDB
from spec2chat.utils.openai_config import configure_openai

configure_openai()

# Obtener la base de datos
db = MongoDB()

def service_selection(tagServices, user_input, slots, intent, domain):
    service_descriptions = {}
    services = db.get_collection(domain, 'services')

    # Cojo los servicios con los valores máximo del vector
    max_value = max(tagServices.values())
    max_keys = [key for key, value in tagServices.items() if value == max_value]
    selected_services = []

    # Miro a ver cuantos servicios han salido con etiquetas máximas
    # Si es mayor que uno
    if len(max_keys) > 1:
        print("Entro porque hay más de un servicio")
        for service_id in max_keys:
            print("Servicio a estudiar")
            print(service_id)
            # Busco el servicio por id
            document = services.find_one({"_id": ObjectId(service_id)})

            # Check if the document exists and contains 'paths'
            if document and 'paths' in document:
                # Iterar sobre todos los endpoints disponibles
                for path, methods in document["paths"].items():
                    print(f"Revisando path: {path}")

                    # Para cada método (get, post) en el endpoint
                    for method, details in methods.items():
                        print(f"Revisando método: {method}")

                        parameters = details.get("parameters", [])
                        examples = {}

                        # Guardar ejemplos dinámicamente
                        for param in parameters:
                            param_name = param["name"]
                            if "x-value" in param["schema"]:
                                examples[param_name] = param["schema"]["x-value"]

                        # Verificar coincidencias con los slots del usuario
                        match_found = False
                        for slot_name, slot_value in slots.items():
                            if slot_name in examples and examples[slot_name] == slot_value:
                                print(f"Matching slot: {slot_name} with value: {slot_value}")
                                match_found = True
                                break  # Stop if a match is found

                        if match_found:
                            print(f"Service {service_id} matches the user's slot values")
                            selected_services.append(service_id)

    else:
        selected_services = [max_keys[0]]

    if not selected_services:
        random_service = random.choice(list(tagServices.keys()))
        selected_services.append(random_service)

    print("SELECTED SERVICES")
    print(selected_services)
    return selected_services

def select_service_by_intent(intent, domain):
    services = []
    services_ = db.get_collection(domain, 'services')
    #cojo todos los elementos de la base de datos de mongo
    all_services = services_.find({'paths': {'$exists': True}})
    print("sacando los servicios para el intent: " + intent + " y el dominio: " + domain)
    print(all_services)
    for document in all_services:
        for i in document['paths']:
            # Check if the 'paths' field exists and is a dictionary
            if 'paths' in document and isinstance(document['paths'], dict):
                # Iterate over each path in the document
                for path, _ in document['paths'].items():
                    # Remove the leading '/' character from the path
                    intent_name_without_char = path.lstrip('/')
                    if (intent_name_without_char == intent):
                        services.append(document['_id'])
    return services