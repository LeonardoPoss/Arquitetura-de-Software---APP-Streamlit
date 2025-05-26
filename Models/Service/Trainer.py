import pandas as pd
import streamlit as st
from pycaret.classification import setup as class_setup, compare_models as class_compare
from pycaret.regression import setup as reg_setup, compare_models as reg_compare
from pycaret.clustering import setup as clus_setup, create_model as clus_create

class PyCaretTrainer:
    def __init__(self):
        self.model = None

    def train_model(self, df: pd.DataFrame, target: str, task_type: str):
        with st.spinner("🔄 Treinando modelo, aguarde..."):
            if task_type == "classification":
                class_setup(data=df, target=target, session_id=123, html=False)
                self.model = class_compare()
                st.success("✅ Modelo de Classificação treinado com sucesso!")
                st.write(self.model)

            elif task_type == "regression":
                reg_setup(data=df, target=target, session_id=123, html=True, silent=True)
                self.model = reg_compare()
                st.success("✅ Modelo de Regressão treinado com sucesso!")
                st.write(self.model)

            elif task_type == "clustering":
                clus_setup(data=df, session_id=123, html=True, silent=True)
                self.model = clus_create("kmeans")
                st.success("✅ Modelo de Cluster treinado com sucesso!")
                st.write(self.model)

            else:
                st.error("❌ Tipo de tarefa inválido: escolha entre classification, regression ou clustering")
                raise ValueError("Tipo de tarefa inválido.")

        return self.model
