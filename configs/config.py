from dotenv import load_dotenv
load_dotenv()

import os
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
WANDB_API_KEY = os.getenv("WANDB_API_KEY")
AWS_ACC_KEY = os.getenv("AWS_ACC_KEY")
AWS_SEC_KEY = os.getenv("AWS_SEC_KEY")
os.environ["AWS_DEFAULT_REGION"] = "ap-northeast-1"
GEMINIE_API_KEY = os.getenv("GEMINI_API_KEY")
