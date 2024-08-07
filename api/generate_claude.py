import boto3
import json
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

import sys
sys.path.append("/workspace/configs")
import config

def output_model_list(region_name: str="ap-northeast-1"):
    bedrock = boto3.client(service_name='bedrock', region_name=region_name, aws_access_key_id=config.AWS_ACC_KEY, aws_secret_access_key=config.AWS_SEC_KEY)
    return [[model_dict["providerName"], model_dict["modelId"], model_dict["inputModalities"]] for model_dict in bedrock.list_foundation_models()["modelSummaries"]]

def format_claude_v2_prompt(prompt):
    """
    Claudev2のフォーマット
    Human: {prompt}\n\nAssistant:
    """

    return f"Human: {prompt}\n\nAssistant:"

def format_claude_v3_prompt(prompt, MAX_NEW_TOKEN):
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": MAX_NEW_TOKEN,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        }
    )
    return body

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def claude_v3_chat_complettion(model, prompt, **kwargs):
    bedrock = boto3.client(service_name='bedrock-runtime', region_name="us-east-1", aws_access_key_id=config.AWS_ACC_KEY, aws_secret_access_key=config.AWS_SEC_KEY)
    body = prompt
    modelId = model
    accept = 'application/json'
    contentType = 'application/json'

    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    response_body = json.loads(response.get('body').read())
    return response_body

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def claude_v2_chat_complettion(model, prompt, **kwargs):
    if model in ["anthropic.claude-instant-v1:2:18k", "anthropic.claude-instant-v1", "anthropic.claude-v2:1:18k", "anthropic.claude-v2:1:200k", "anthropic.claude-v2:1"]:
        bedrock = boto3.client(service_name='bedrock-runtime', aws_access_key_id=config.AWS_ACC_KEY, aws_secret_access_key=config.AWS_SEC_KEY)
    else:
        bedrock = boto3.client(service_name='bedrock-runtime', region_name="us-east-1", aws_access_key_id=config.AWS_ACC_KEY, aws_secret_access_key=config.AWS_SEC_KEY)
    body = json.dumps({
        "prompt": prompt,
        **kwargs
    })
    modelId = model
    accept = 'application/json'
    contentType = 'application/json'

    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

    response_body = json.loads(response.get('body').read())
    return response_body
