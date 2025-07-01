import json
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from schema import OnboardingSurvey, onboarding_schema_format_instructions
from llm.models import survey_model
from llm.prompts.survey_gen import survey_prompt

load_dotenv()

messages = [
    HumanMessage(
        content=survey_prompt.format(
            description="Sou um músico de 18 anos apaixonado por violino.",
            intentions="me expressar melhor | me distrair com perguntas legais",
            output_format=onboarding_schema_format_instructions,
        )
    )
]

response = survey_model.with_structured_output(OnboardingSurvey, include_raw=True).invoke(messages)
onboarding : OnboardingSurvey = response['parsed']
usage_metadata = response['raw'].usage_metadata

print("Resposta do modelo:\n", onboarding.model_dump_json(indent=4))
print()
print("Metadados:")
print("input:", json.dumps(usage_metadata['input_tokens'], ensure_ascii=False, indent=4))
print("output:", json.dumps(usage_metadata['output_tokens'], ensure_ascii=False, indent=4))
print("total:", json.dumps(usage_metadata['total_tokens'], ensure_ascii=False, indent=4))

