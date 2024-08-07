import google.generativeai as genai
import json
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

import sys
sys.path.append("/workspace/configs")


import config

GEMINIE_API_KEY = config.GEMINIE_API_KEY
genai.configure(api_key=GEMINIE_API_KEY)

def configure_model(model_name: str="gemini-1.5-pro-latest"):
    model = genai.GenerativeModel(model_name)
    chat = model.start_chat(history=[])
    return model, chat

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_content(model: str, prompt: str, **kwargs):
    response = model.generate_content(prompt, **kwargs)
    return response

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_chat_content(chat, prompt: str, **kwargs):
    response = chat.send_message(prompt, **kwargs)
    return response
