from uuid import uuid4
from streamlit_local_storage import LocalStorage

class StorageManager:
    def __init__(self):
        self.storage = LocalStorage()
    
    def save_user_data(self, nome: str, intencoes: list) -> dict:
        """
        Salva os dados do usuário no local storage
        
        Args:
            nome: Nome do usuário
            intencoes: Lista de intenções selecionadas
            
        Returns:
            dict: Dados do usuário salvos
        """
        user_id = str(uuid4())
        user_data = {
            "id": user_id,
            "nome": nome,
            "intencoes": intencoes
        }
        
        self.storage.setItem("user_data", user_data)
        return user_data
