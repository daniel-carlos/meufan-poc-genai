from dotenv import load_dotenv
load_dotenv()
from schema import OnboardingSurvey, onboarding_schema_format_instructions
from llm.models import survey_model
from llm.prompts.survey_gen import survey_prompt

chain = survey_prompt | survey_model.with_structured_output(OnboardingSurvey)

onboarding_survey: OnboardingSurvey = chain.invoke(
    {
        "description": "Sou um músico de 18 anos apaixonado por violino.",
        "intentions": "me expressar melhor | me distrair com perguntas legais",
        "output_format": onboarding_schema_format_instructions,
    }
)

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


pretty_print_survey(onboarding_survey)


# pydantic_parser = PydanticOutputParser(pydantic_object=OnboardingSurvey)
# format_instructions = pydantic_parser.get_format_instructions()
# print(format_instructions)
