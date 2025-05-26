import os
import streamlit as st

from Controllers.Autenticador import KaggleAuthenticator  

class KaggleDownloader:
    def __init__(self, dataset_name, pasta_destino=None):
        """
        Inicializa o downloader com o nome do dataset e pasta destino.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório atual do script
        if pasta_destino is None:
            pasta_destino = os.path.join(base_dir, '..', 'Models', 'Dataset')  # Caminho relativo mais estável

        self.dataset_name = dataset_name
        self.pasta_destino = os.path.abspath(pasta_destino)
        self.authenticator = KaggleAuthenticator()
        self.api = self.authenticator.get_api()

        try:
            os.makedirs(self.pasta_destino, exist_ok=True)
            st.info(f"📂 Diretório para download: `{self.pasta_destino}`")
        except Exception as e:
            st.error(f"❌ Erro ao criar diretório `{self.pasta_destino}`: {e}")
            st.stop()

    def verificar_e_baixar_dataset(self):
        """
        Verifica se o dataset já existe localmente e, se não, baixa do Kaggle.
        """
        extensoes_validas = {".csv", ".json", ".xlsx", ".zip", ".txt"}

        try:
            st.info(f"📥 Baixando dataset: `{self.dataset_name}`...")
            self.api.dataset_download_files(self.dataset_name, path=self.pasta_destino, unzip=True)

            arquivos_existentes = [
                f for f in os.listdir(self.pasta_destino)
                if os.path.isfile(os.path.join(self.pasta_destino, f)) 
                and os.path.splitext(f)[1] in extensoes_validas
            ]

            if arquivos_existentes:
                st.success(f"✅ Download concluído! Arquivos salvos em `{self.pasta_destino}`.")
            else:
                st.warning("⚠️ O download foi feito, mas nenhum arquivo válido foi encontrado na pasta.")
        except Exception as e:
            st.error(f"❌ Erro ao baixar o dataset: {e}")
