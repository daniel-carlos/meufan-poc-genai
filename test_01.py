import os
from dotenv import load_dotenv
from schema import OnboardingSurvey

load_dotenv()

from llm.models import survey_model
import json

onboarding_survey: OnboardingSurvey = survey_model.with_structured_output(
    OnboardingSurvey
).invoke("**Quem é você?** Sou um músico de 18 anos apaixonado por violino.\n **Qual é sua intenção aqui?** me expressar melhor e me distrair com perguntas legais")

print(json.dumps(onboarding_survey.model_dump(), indent=2, ensure_ascii=False))