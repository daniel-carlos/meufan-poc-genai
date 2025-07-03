from langchain_groq import ChatGroq
from langchain_aws import ChatBedrockConverse
import os
from dotenv import load_dotenv
load_dotenv()

survey_model = ChatBedrockConverse(
    model=os.environ.get("SURVEY_MODEL_ID", "amazon.nova-lite-v1:0"),
    temperature=os.environ.get("SURVEY_MODEL_TEMPERATURE", 0.9),
    max_tokens=None,
    cache=False,
)
