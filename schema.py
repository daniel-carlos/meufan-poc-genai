from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class InterestTag(str, Enum):
    EMOCOES = "emoções"
    MUSICA = "música"
    FILMES_SERIES = "filmes e séries"
    ESPIRITUALIDADE = "espiritualidade"
    AUTOCONHECIMENTO = "autoconhecimento"
    FILOSOFIA = "filosofia"
    RELACIONAMENTOS = "relacionamentos"
    VIDA_PROFISSIONAL = "vida profissional"
    TECNOLOGIA = "tecnologia"
    CULTURA_POP = "cultura pop"
    SAUDE_MENTAL = "saúde mental"
    PETS = "pets"
    POLITICA = "política"
    VIAGENS = "viagens"
    ESPORTES = "esportes"


class OnboardingSurvey(BaseModel):
    """Pesquisa de onboarding para coletar informações do usuário a fim de traçar um perfil."""

    title: str = Field(
        ...,
        description="Títlo atribuído ao usuário.",
        examples=["idoso amante de pássaros"],
    )
    customer_profile: bool = Field(
        ..., description="Identfica se é um perfil consumidor."
    )
    profile_questions: list[str] = Field(
        ...,
        description="Perguntas a serem feita ao usuário considerando apenas seu perfil.",
        min_length=5,
        max_length=5,
    )
    general_questions: list[str] = Field(
        ...,
        description="Perguntas complementares diversas a serem feita ao usuário. Perguntas fora do perfil com objetivo de entender melhor o usuário.",
        min_length=5,
        max_length=5,
    )
    customer_questions: list[str] = Field(
        ...,
        description="Perguntas sobre o perfil de consumo do usuário. Tem objetivo de entender o perfil de consumo do usuário.",
        min_length=2,
        max_length=2,
    )
    interest_tags: list[InterestTag] = Field(
        ...,
        description="Tags de interesse associadas a esse usuário.",
        min_length=3,
        max_length=3,
    )
