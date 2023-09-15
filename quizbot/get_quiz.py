import json
from typing import Dict

import openai
import test_data as td

chat_history = [
    {
        "role": "system",
        "content": "You are a REST API server with an endpoint /generate-random-question?data={data:""}, which generates unique random quiz question based on the query parameter data in json data. Note that the explanation generated must be able to be found in the query parameter data.",
    },
    {
        "role": "user",
        "content": f"GET /generate-random-question/?data={{'data': '{td.devops_notes}'}}"
    },    
    {
        "role": "assistant",
        "content": '\n\n{\n    "question": "What is Docker primarily used for?",\n    "options": ["Running virtual machines", "Creating and managing containers", "Orchestrating containers in a cluster", "Developing mobile applications"],\n    "answer": "Creating and managing containers",\n    "explanation": "ocker is primarily used for creating and managing containers, which are lightweight, portable environments for running applications and their dependencies."\n}',
    },
    {
        "role": "user", 
        "content": f"GET /generate-random-question/?data={{'data': '{td.jenkins_notes}'}}"
    },
    {
        "role": "assistant",
        "content": '\n\n{\n    "question": "What is the primary purpose of Jenkins in software development?",\n    "options": ["Managing project documentation", "Automating and streamlining the software development and delivery process", "Providing version control for code", "Creating graphical user interfaces (GUIs)"],\n    "answer": "Automating and streamlining the software development and delivery process",\n    "explanation": "Jenkins is primarily used for automating and streamlining various stages of the software development and delivery pipeline, including continuous integration, automated testing, and deployment."\n}',
    },
]


def get_quiz_from_data(data, api_key) -> Dict[str, str]:
    global chat_history
    openai.api_key = api_key
    current_chat = chat_history[:]
    current_user_message = {
        "role": "user",
        "content": f"GET /generate-random-question?data={data}",
    }
    current_chat.append(current_user_message)
    chat_history.append(current_user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=current_chat
    )
    quiz = response["choices"][0]["message"]["content"]
    current_assistent_message = {"role": "assistant", "content": quiz}
    chat_history.append(current_assistent_message)
    print(f"Response:\n{quiz}")
    return json.loads(quiz)