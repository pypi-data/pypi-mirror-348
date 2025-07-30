"""
spec2chat - A Python library for building task-oriented conversational systems from OpenAPI service specifications.

Author: M. Jesús Rodríguez
License: Apache 2.0 License
Version: 0.1.6
Repository: https://github.com/mjesusrodriguez/spec2chat
Created on 17/05/2025 by M. Jesús Rodríguez

This example shows how to use the `run_chatbot` function from the `spec2chat` package
to interact with a user request and complete a task-oriented conversation.
"""

from dotenv import load_dotenv
load_dotenv()

from spec2chat import run_chatbot

def main():
    user_input = "I want a cheap vegetarian restaurant"
    user_answers = []
    filledslots = {}

    print("\n[Step 0] Sending initial user message:")
    response = run_chatbot(user_input=user_input)
    print("[Step 1] Chatbot response:")
    print(response)

    tasks = response.get("tasks", {})
    domain = response.get("dom", "")
    intent = response.get("intent", "")
    reqslots = response.get("reqslots", [])
    services = response.get("services", [])

    step = 2
    while not response.get("end_of_conversation", False):
        print(f"\n[Step {step}] Sending answers to new questions...")

        simulated_answers = {
            "name": "John Doe",
            "phone": "123456789",
            "date": "2024-06-01",
            "time": "19:30",
            "diners": "2",
            "location": "terrace",
            "food": "vegetarian",
            "pricerange": "cheap",
            "terrace": "yes",
            "petfriendly": "no",
            "smokingzone": "no",
            "smoking": "no"
        }

        for slot, question in response.get("questions", {}).items():
            answer = simulated_answers.get(slot, "test")
            user_answers.append({"chatbot": question, "user": answer})
            filledslots[slot] = answer

        response = run_chatbot(
            user_input=user_input,
            user_answers=user_answers,
            tasks=response.get("tasks", tasks),
            domain=response.get("dom", domain),
            intent=response.get("intent", intent),
            filledslots=filledslots,
            services=response.get("services", services),
            reqslots=response.get("reqslots", reqslots),
            service_id=response.get("service_id")
        )

        print(f"[Step {step}] Chatbot response:")
        print(response)

        if response.get("final") and not response.get("questions"):
            print("[DEBUG] Finished: all slots are filled and no more questions are pending.")
            break

        step += 1

    if response.get("end_of_conversation"):
        print("\nConversation successfully completed.")
    else:
        print("\nConversation incomplete or could not continue.")

if __name__ == "__main__":
    main()