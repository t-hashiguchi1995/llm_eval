import openai
import json
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import sys
sys.path.append("/workspace/configs")

import config

client = openai.OpenAI(api_key=config.OPENAI_API_KEY)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def chat_complettion(model:str, user_prompt:str, system_prompt:str="You are a helpful assistant.", **kwargs):
    response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    **kwargs
    )
    response_json = json.loads(response.json())
    return response_json
