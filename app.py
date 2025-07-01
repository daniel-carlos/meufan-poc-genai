import streamlit as st
from core import setup_page, FormularioOnboarding

# Configuração da página
setup_page()

# Título da aplicação
st.title("📝 Formulário de Onboarding")
st.markdown("---")

# Inicialização do formulário
formulario = FormularioOnboarding()

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

