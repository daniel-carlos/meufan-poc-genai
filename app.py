import streamlit as st
from core import setup_page, FormularioOnboarding
from dotenv import load_dotenv

load_dotenv()

# Configuração da página
setup_page()

# Inicialização do formulário
formulario = FormularioOnboarding()

# Controle de navegação
if "survey_generated" not in st.session_state:
    st.session_state.survey_generated = False

# Verificar qual tela mostrar
if st.session_state.survey_generated:
    # Mostrar tela da survey
    formulario.render_survey_screen()
else:
    # Mostrar formulário inicial
    st.title("📝 Formulário de Onboarding")
    st.markdown("---")

    # Formulário
    with st.form("formulario_identificacao"):
        st.subheader("Por favor, responda às seguintes perguntas:")

        # Campo de nome
        nome = formulario.render_name_input()

        # Checkboxes de intenções
        intencoes_selecionadas = formulario.render_intentions_checkboxes()

        # Botão de envio
        submitted = st.form_submit_button("Enviar", type="primary")

        # Processamento do formulário
        if submitted:
            formulario.process_submission(nome, intencoes_selecionadas)

# Rodapé
st.markdown("---")
st.caption("Formulário criado com Streamlit")
