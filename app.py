import streamlit as st
from uuid import uuid4
from streamlit_local_storage import LocalStorage

localS = LocalStorage()

# Configuração da página
st.set_page_config(page_title="Formulário de Identificação", page_icon="📝")

# Título da aplicação
st.title("📝 Formulário de Identificação")
st.markdown("---")

# Formulário
with st.form("formulario_identificacao"):
    st.subheader("Por favor, responda às seguintes perguntas:")
    
    # Pergunta 1
    nome = st.text_input(
        "**Quem é você?**",
        placeholder="Digite seu nome ou como gostaria de ser chamado..."
    )
    
    # Pergunta 2
    st.markdown("**Qual é sua intenção aqui?** *(Selecione 1 ou 2 opções)*")
    
    opcoes_intencao = {
        "me_expressar": "Me expressar melhor",
        "guardar_memorias": "Guardar minhas memórias",
        "me_conhecer": "Me conhecer mais",
        "me_distrair": "Me distrair com perguntas legais",
        "ter_ideias": "Ter ideias novas",
        "inspirar_outros": "Inspirar outras pessoas",
        "relaxar_refletir": "Relaxar e refletir"
    }
    
    # Verificar quantos checkboxes estão marcados
    intencoes_selecionadas = []
    checkboxes_values = {}
    
    # Primeiro loop para capturar os valores atuais
    for key, label in opcoes_intencao.items():
        if key in st.session_state:
            checkboxes_values[key] = st.session_state[key]
        else:
            checkboxes_values[key] = False
    
    # Contar quantos estão selecionados
    count_selected = sum(checkboxes_values.values())
    
    # Segundo loop para criar os checkboxes com disabled quando necessário
    for key, label in opcoes_intencao.items():
        # Desabilitar se 2 já estão selecionados E este não está selecionado
        disabled = count_selected >= 2 and not checkboxes_values[key]
        
        if st.checkbox(label, key=key, disabled=disabled):
            intencoes_selecionadas.append(label)
    
    # Botão de envio
    submitted = st.form_submit_button("Enviar", type="primary")
    
    # Processamento do formulário
    if submitted:
        if nome and intencoes_selecionadas:
            # Validar quantidade de opções selecionadas (redundante, mas mantido por segurança)
            if len(intencoes_selecionadas) > 2:
                st.error("❌ Por favor, selecione no máximo 2 opções!")
            else:
                # Gerar ID único para o usuário
                user_id = str(uuid4())
                
                # Salvar dados no local storage
                user_data = {
                    "id": user_id,
                    "nome": nome,
                    "intencoes": intencoes_selecionadas
                }
                
                try:
                    localS.setItem("user_data", user_data)
                    st.success("✅ Obrigado pelas informações!")
                    st.balloons()
                    
                    # Mostrar dados salvos
                    st.markdown("### Informações registradas:")
                    st.write(f"**Nome:** {nome}")
                    st.write(f"**Intenções:** {', '.join(intencoes_selecionadas)}")
                    st.write(f"**ID:** {user_id}")
                    
                except Exception as e:
                    st.error(f"Erro ao salvar dados: {e}")
                
        else:
            if not nome:
                st.error("❌ Por favor, preencha seu nome!")
            if not intencoes_selecionadas:
                st.error("❌ Por favor, selecione pelo menos uma intenção!")

# Rodapé
st.markdown("---")
st.caption("Formulário criado com Streamlit")

