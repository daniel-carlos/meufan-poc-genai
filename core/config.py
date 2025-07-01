import streamlit as st

def setup_page():
    """Configura as configurações iniciais da página"""
    st.set_page_config(page_title="Formulário de Identificação", page_icon="📝")

OPCOES_INTENCAO = {
    "me_expressar": "Me expressar melhor",
    "guardar_memorias": "Guardar minhas memórias",
    "me_conhecer": "Me conhecer mais",
    "me_distrair": "Me distrair com perguntas legais",
    "ter_ideias": "Ter ideias novas",
    "inspirar_outros": "Inspirar outras pessoas",
    "relaxar_refletir": "Relaxar e refletir"
}
