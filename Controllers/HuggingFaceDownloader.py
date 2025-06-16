# Controllers/HuggingFaceDownloader.py

import os
import pandas as pd
from datasets import load_dataset
import streamlit as st

class HuggingFaceDownloader:
    def __init__(self, dataset_name, split="train", pasta_destino="Models/Dataset"):
        self.dataset_name = dataset_name
        self.split = split
        self.pasta_destino = pasta_destino
        os.makedirs(self.pasta_destino, exist_ok=True)

    def baixar_e_salvar(self):
        try:
            st.info(f"🔄 Baixando `{self.dataset_name}` da Hugging Face...")
            dataset = load_dataset(self.dataset_name, split=self.split)

            # Converter para DataFrame
            df = dataset.to_pandas()

            # Salvar como CSV
            nome_arquivo = self.dataset_name.replace("/", "_") + ".csv"
            caminho_completo = os.path.join(self.pasta_destino, nome_arquivo)
            df.to_csv(caminho_completo, index=False)

            st.success(f"✅ Dataset `{self.dataset_name}` salvo em `{caminho_completo}`.")
            return caminho_completo
        except Exception as e:
            st.error(f"❌ Erro ao baixar dataset do Hugging Face: {e}")
            return None
