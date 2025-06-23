from os import environ
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

TITLE = environ.get("TITLE", "Assistente Virtual")
SUBTITLE = environ.get("SUBTITLE", "Bem vindo ao assistente virtual!")
PASSWORD = environ.get("PASSWORD", "123")
DYNAMODB_TABLE = environ.get("DYNAMODB_TABLE")
DYNAMODB_REGION = environ.get("DYNAMODB_REGION", "us-east-1")
BEDROCK_MODEL_ID = environ.get("BEDROCK_MODEL_ID", "amazon.nova-pro-v1:0")
BEDROCK_REGION = environ.get("BEDROCK_REGION", "us-east-1")
BEDROCK_MODEL_TEMPERATURE = environ.get("BEDROCK_MODEL_TEMPERATURE", "0.7")
BEDROCK_MODEL_MAX_TOKENS = environ.get("BEDROCK_MODEL_MAX_TOKENS", "500")
BEDROCK_KB_ID = environ.get("BEDROCK_KB_ID")
BEDROCK_KB_MAX_RESULTS = environ.get("BEDROCK_KB_MAX_RESULTS", "4")
BEDROCK_AGENT_PROMPT = environ.get("BEDROCK_AGENT_PROMPT", "Você é um assistente virtual prestativo e amigável.")