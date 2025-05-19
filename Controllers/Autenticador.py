import os
import json
import streamlit as st
from kaggle.api.kaggle_api_extended import KaggleApi  

class KaggleAuthenticator:
    def __init__(self, cred_path="Login_kaggle/kaggle.json"):
        """Inicializa o autenticador Kaggle com um caminho específico para as credenciais."""
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.cred_path = os.path.join(self.base_dir, cred_path)

    def carregar_credenciais(self):
        """Carrega as credenciais do arquivo JSON e define as variáveis de ambiente."""
        if not os.path.exists(self.cred_path):
            st.error(f"❌ Arquivo de credenciais não encontrado: {self.cred_path}")
            raise FileNotFoundError(f"Arquivo {self.cred_path} não encontrado.")

        with open(self.cred_path, "r", encoding="utf-8") as f:
            dados = json.load(f)

        os.environ["KAGGLE_USERNAME"] = dados["username"]
        os.environ["KAGGLE_KEY"] = dados["key"]
        st.success("✅ Credenciais do Kaggle carregadas com sucesso!")

    def get_api(self):
        """Retorna uma instância autenticada da API do Kaggle."""
        try:
            self.carregar_credenciais()
            api = KaggleApi()
            api.authenticate()
            st.success("🔐 Autenticação no Kaggle realizada com sucesso!")
            return api
        except Exception as e:
            st.error(f"❌ Erro ao autenticar no Kaggle: {e}")
            return None
