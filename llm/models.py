from langchain_groq import ChatGroq
import os

survey_model = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    temperature=0.9,
    max_tokens=None,
    reasoning_format="parsed",
    cache=False,
    streaming=False,
    timeout=None,
    max_retries=2,
    api_key=os.environ["GROQ_API_KEY"],
)
