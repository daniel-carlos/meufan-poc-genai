

def generate_survey(description, intentions):
    from llm.models import SurveyModel
    from llm.prompts.survey_gen import survey_prompt
    from schema import SurveySchema
    from langchain_core.messages import HumanMessage
    from schema import OnboardingSurvey, onboarding_schema_format_instructions
    from llm.models import survey_model
    from llm.prompts.survey_gen import survey_prompt

    # Initialize the survey model
    messages = [
    HumanMessage(
            content=survey_prompt.format(
                description=description,
                intentions=" | ".join(intentions),
                output_format=onboarding_schema_format_instructions,
            )
        )
    ]

    response = survey_model.with_structured_output(OnboardingSurvey, include_raw=True).invoke(messages)
    onboarding : OnboardingSurvey = response['parsed']
    usage_metadata = response['raw'].usage_metadata

    return onboarding, usage_metadata