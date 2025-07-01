from dotenv import load_dotenv

load_dotenv()
from schema import OnboardingSurvey, onboarding_schema_format_instructions
from llm.models import survey_model
from llm.prompts.survey_gen import survey_prompt

def pretty_print_survey(survey: OnboardingSurvey):
    print(f"Title: {survey.title}")
    print(f"Customer Profile: {survey.customer_profile}")
    print("Profile Questions:")
    for question in survey.profile_questions:
        print(f"- {question}")
    print("General Questions:")
    for question in survey.general_questions:
        print(f"- {question}")
    print("Customer Questions:")
    for question in survey.customer_questions:
        print(f"- {question}")
    print("Interest Tags:")
    for tag in survey.interest_tags:
        print(f"- {tag.value}")


survey_input = {
    "description": "Sou um músico de 18 anos apaixonado por violino.",
    "intentions": "me expressar melhor | me distrair com perguntas legais",
    "output_format": onboarding_schema_format_instructions,
}

survey_prompt_input = survey_prompt.invoke(survey_input).messages[0].content
print("Input:\n", survey_prompt_input)

input_tokens = survey_model.get_num_tokens(survey_prompt_input)
print(f"Tokens de entrada: {input_tokens}")