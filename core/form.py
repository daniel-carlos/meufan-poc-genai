import streamlit as st
from .config import OPCOES_INTENCAO
from .storage import StorageManager

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
                user_data = self.storage_manager.save_user_data(nome, intencoes)
                self.show_success_message(user_data)
            except Exception as e:
                st.error(f"Erro ao salvar dados: {e}")
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
