import streamlit as st
from .config import OPCOES_INTENCAO
from .storage import StorageManager
from .llm import generate_survey

class FormularioOnboarding:
    def __init__(self):
        self.storage_manager = StorageManager()
        
    def render_name_input(self):
        """Renderiza o campo de entrada do nome"""
        return st.text_input(
            "**Quem é você?**",
            placeholder="Digite seu nome ou como gostaria de ser chamado..."
        )
    
    def render_intentions_checkboxes(self):
        """Renderiza os checkboxes de intenções"""
        st.markdown("**Qual é sua intenção aqui?** *(Selecione 1 ou 2 opções)*")
        
        intencoes_selecionadas = []
        checkboxes_values = {}
        
        # Primeiro loop para capturar os valores atuais
        for key, label in OPCOES_INTENCAO.items():
            if key in st.session_state:
                checkboxes_values[key] = st.session_state[key]
            else:
                checkboxes_values[key] = False
        
        # Contar quantos estão selecionados
        count_selected = sum(checkboxes_values.values())
        
        # Segundo loop para criar os checkboxes com disabled quando necessário
        for key, label in OPCOES_INTENCAO.items():
            # Desabilitar se 2 já estão selecionados E este não está selecionado
            disabled = count_selected >= 2 and not checkboxes_values[key]
            
            if st.checkbox(label, key=key, disabled=disabled):
                intencoes_selecionadas.append(label)
                
        return intencoes_selecionadas
    
    def process_submission(self, nome: str, intencoes: list):
        """Processa o envio do formulário"""
        if nome and intencoes:
            if len(intencoes) > 2:
                st.error("❌ Por favor, selecione no máximo 2 opções!")
                return
            
            try:
                # Salvar dados do usuário
                user_data = self.storage_manager.save_user_data(nome, intencoes)
                
                # Gerar survey usando IA
                with st.spinner("🤖 Gerando questões personalizadas para você..."):
                    description = f"Usuário chamado {nome}"
                    survey, usage_metadata = generate_survey(description, intencoes)
                
                # Armazenar survey no session_state
                st.session_state.survey_generated = True
                st.session_state.user_data = user_data
                st.session_state.survey = survey
                st.session_state.usage_metadata = usage_metadata
                
                # Rerun para mostrar a nova tela
                st.rerun()
                
            except Exception as e:
                st.error(f"Erro ao processar formulário: {e}")
        else:
            self.show_validation_errors(nome, intencoes)
    
    def show_success_message(self, user_data: dict):
        """Mostra a mensagem de sucesso e os dados salvos"""
        st.success("✅ Obrigado pelas informações!")
        st.balloons()
        
        st.markdown("### Informações registradas:")
        st.write(f"**Nome:** {user_data['nome']}")
        st.write(f"**Intenções:** {', '.join(user_data['intencoes'])}")
        st.write(f"**ID:** {user_data['id']}")
    
    def show_validation_errors(self, nome: str, intencoes: list):
        """Mostra mensagens de erro de validação"""
        if not nome:
            st.error("❌ Por favor, preencha seu nome!")
        if not intencoes:
            st.error("❌ Por favor, selecione pelo menos uma intenção!")
    
    def render_survey_screen(self):
        """Renderiza a tela com as questões geradas pela IA"""
        survey = st.session_state.survey
        user_data = st.session_state.user_data
        
        # Cabeçalho
        st.title("🎯 Suas Questões Personalizadas")
        st.markdown(f"**Olá, {user_data['nome']}!** Preparamos algumas perguntas especiais para você.")
        st.markdown(f"**Seu perfil:** {survey.title}")
        st.markdown("---")
        
        # Formulário com as questões
        with st.form("survey_form"):
            st.subheader("📝 Responda às perguntas abaixo:")
            
            responses = {}
            
            # Perguntas do perfil
            if survey.profile_questions:
                st.markdown("### 🎭 Perguntas sobre seu perfil:")
                for i, question in enumerate(survey.profile_questions):
                    responses[f"profile_{i}"] = st.text_area(
                        f"**{i+1}.** {question}",
                        key=f"profile_q_{i}",
                        height=100
                    )
            
            # Perguntas gerais
            if survey.general_questions:
                st.markdown("### 💭 Perguntas gerais:")
                for i, question in enumerate(survey.general_questions):
                    responses[f"general_{i}"] = st.text_area(
                        f"**{i+1}.** {question}",
                        key=f"general_q_{i}",
                        height=100
                    )
            
            # Perguntas de consumo (se aplicável)
            if survey.customer_profile and survey.customer_questions:
                st.markdown("### 🛍️ Perguntas sobre consumo:")
                for i, question in enumerate(survey.customer_questions):
                    responses[f"customer_{i}"] = st.text_area(
                        f"**{i+1}.** {question}",
                        key=f"customer_q_{i}",
                        height=100
                    )
            
            # Botões de ação
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("📤 Enviar Respostas", type="primary"):
                    self.process_survey_responses(responses)
            
            with col2:
                if st.form_submit_button("🔄 Gerar Novas Questões"):
                    st.session_state.survey_generated = False
                    st.rerun()
        
        # Mostrar informações adicionais
        self.show_survey_info(survey)
    
    def process_survey_responses(self, responses: dict):
        """Processa as respostas da survey"""
        # Filtrar respostas vazias
        filled_responses = {k: v for k, v in responses.items() if v.strip()}
        
        if not filled_responses:
            st.error("❌ Por favor, responda pelo menos uma pergunta!")
            return
        
        try:
            # Aqui você pode salvar as respostas ou processá-las
            st.success("✅ Respostas enviadas com sucesso!")
            st.balloons()
            
            # Mostrar resumo das respostas
            st.markdown("### 📊 Suas respostas:")
            for key, value in filled_responses.items():
                st.write(f"**{key}:** {value[:100]}{'...' if len(value) > 100 else ''}")
            
            # Opção para reiniciar
            if st.button("🏠 Voltar ao início"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
                
        except Exception as e:
            st.error(f"Erro ao processar respostas: {e}")
    
    def show_survey_info(self, survey):
        """Mostra informações adicionais sobre a survey"""
        with st.expander("ℹ️ Informações da Survey"):
            st.write(f"**Perfil do consumidor:** {'Sim' if survey.customer_profile else 'Não'}")
            st.write(f"**Tags de interesse:** {', '.join([tag.value for tag in survey.interest_tags])}")
            st.write(f"**Total de perguntas:** {len(survey.profile_questions) + len(survey.general_questions) + len(survey.customer_questions)}")
