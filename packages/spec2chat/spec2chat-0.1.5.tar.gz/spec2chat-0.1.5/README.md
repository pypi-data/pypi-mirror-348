# spec2chat

**spec2chat** is a Python library for building task-oriented conversational systems based on PPTalk service specifications. It automatically transforms OpenAPI descriptions into dialogue flows with slot filling, service selection, and question generation, powered by GPT-based language models.

The library is designed to simplify the creation of chatbots that interact with web services, allowing developers to focus on business logic and user experience.

---

## Installation

```bash
pip install spec2chat
```

---

## Additional Requirements

After installing the library, you must download the following NLP resources required by `spec2chat`:

```bash
# Lexical database used for tag extraction
python -m nltk.downloader wordnet

# Lightweight English model for spaCy (required for tag and synonym detection)
python -m spacy download en_core_web_sm

# (Optional) Medium-size model for improved semantic similarity (used in slot ranking)
python -m spacy download en_core_web_md
```

---

## Required Database

The system expects a MongoDB database organized by domain (`hotels`, `restaurants`, etc.) with the following collections:

- `services`: OpenAPI specifications of the conversational services.
- `intents`: list of available intents per domain.
- `slot_ranking`: discriminative parameters with usage frequencies.

---

## Environment Configuration

Before using the library, make sure to define the following environment variables:

```bash
export OPENAI_API_KEY=sk-...
export MONGODB_URI="mongodb://localhost:27017"
```

You can also use the `.env.example` file as a template.  
Simply copy and rename it to `.env`:

```bash
cp .env.example .env
```

If you're using `python-dotenv`, it will be automatically loaded at runtime.

---

## Example Data and Auto-loading

You can find sample data to populate your MongoDB database in the [`/data`](./data/) folder.  
To load them automatically, run:

```bash
python scripts/load_example_data.py
```

---

## Public API

The main public interface of `spec2chat` is the function:

```python
from spec2chat import run_chatbot
```

This is the only function you need to orchestrate a complete, dynamic, task-oriented conversational flow based on OpenAPI service specifications.

All internal components (e.g., slot filling, intent detection, service selection, etc.) are encapsulated and managed automatically.

### Function signature:

```python
run_chatbot(user_input: str, **dialogue_state) -> dict
```

### Usage pattern:

- On the **first call**, provide only the user's input:

  ```python
  run_chatbot("I want a vegetarian restaurant")
  ```

- On subsequent calls, pass the updated dialogue state returned from the previous step (e.g. `filledslots`, `intent`, `useranswers`, etc.) along with the same `user_input`.

- Repeat until the returned object includes:

  ```json
  { "end_of_conversation": true }
  ```

### Returns:

A dictionary representing the current state and next action of the dialogue.  
See the [Sample Outputs](#sample-outputs) section for all possible formats.

---

## Basic Usage

```python
from spec2chat.core.orchestrator import run_chatbot

user_input = "I want a cheap vegetarian restaurant"
user_answers = []

response = run_chatbot(user_input, user_answers=user_answers)
print(response)
```

---

### Sample Outputs

Depending on the dialogue stage, `run_chatbot()` may return different structures:

#### Intermediate stage (pending questions for service selection)

```json
{
  "questions": {
    "pricerange": "How much are you willing to spend?",
    "food": "What type of food are you looking for?"
  },
  "filledslots": {
    "food": "vegetarian"
  },
  "intent": "bookrestaurant",
  "userinput": "I want a cheap vegetarian restaurant",
  "dom": "restaurant",
  "reqslots": ["pricerange", "food"],
  "tasks": {
    "restaurant": "bookrestaurant"
  },
  "final": false
}
```

#### Final stage (service selected)

```json
{
  "questions": {
    "time": "What time would you like the reservation?"
  },
  "filledslots": {
    "food": "vegetarian",
    "pricerange": "cheap"
  },
  "service_id": "660fe62a88cdb240e63e5114",
  "intent": "bookrestaurant",
  "dom": "restaurant",
  "tasks": {
    "restaurant": "bookrestaurant"
  },
  "final": true,
  "reqslots": ["food", "pricerange", "time"]
}
```

#### Conversation ended

```json
{
  "end_of_conversation": true
}
```

#### Open-domain interaction

```json
{
  "chatbot_answer": "That's an interesting question! Let me think...",
  "useranswers": [
    {
      "user": "Tell me about the Eiffel Tower",
      "chatbot": "The Eiffel Tower is a famous landmark in Paris..."
    }
  ],
  "dom": "out-of-domain"
}
```

---

## Dialogue Flow

`spec2chat` implements a complete conversational pipeline including:

1. Domain and intent detection
2. Initial slot filling via language models
3. Service selection based on discriminative parameters
4. Tag-based disambiguation and additional question generation
5. Final slot filling using predefined or refined questions
6. Multi-task management across domains
7. Support for open-domain interactions

---

## Package Structure

```
spec2chat/
├── core/
│   └── orchestrator.py
├── db/
│   └── mongo.py
├── data/
│   ├── hotels.services.json
│   ├── hotels.intents.json
│   └── hotels.slot_ranking.json
├── examples/
│   └── basic_usage.py
├── scripts/
│   └── load_example_data.py
├── services/
│   ├── domain.py
│   ├── intent.py
│   ├── slot_filling.py
│   ├── service_selection.py
│   ├── tag_filter.py
│   ├── discriminative_parameters.py
│   ├── open_domain.py
│   ├── question_generation.py
│   └── question_improvement.py
├── utils/
│   └── openai_config.py
├── .env.example
├── README.md
├── setup.py
└── pyproject.toml
```

---

## Examples

See a full usage example in:

```bash
spec2chat/examples/run_restaurant_example.py
```

---

## Academic Reference

This project is based on the research work published in:

Rodríguez-Sánchez, M.J., Callejas, Z., Ruiz-Zafra, A., Benghazi, K. (2025).  
**Combining Generative AI and PPTalk Service Specification for Dynamic and Adaptive Task-Oriented Chatbots**.  
In: Gaaloul, W., Sheng, M., Yu, Q., Yangui, S. (eds) *Service-Oriented Computing*. ICSOC 2024.  
Lecture Notes in Computer Science, vol 15404. Springer, Singapore.  
📎 https://doi.org/10.1007/978-981-96-0805-8_13

---