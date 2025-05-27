import streamlit as st
import os

def selecionar_treinamento(caminho):
    st.subheader("🤖 Treinar Modelo com PyCaret")
    df = None
    if caminho:
        try:
            import pandas as pd
            df = pd.read_csv(caminho)
            nome_dataset = os.path.basename(caminho)
            colunas = df.columns.tolist()
            target = st.selectbox("Selecione a variável target", colunas)
            task_type = st.selectbox("Tipo de tarefa", ["classification", "regression", "clustering"])
            treinar = st.button("Treinar modelo")
            return df, nome_dataset, target, task_type, treinar
        except Exception as e:
            st.error(f"Erro ao carregar dataset: {e}")
    return df, None, None, None, False

def mostrar_resultado_treinamento(modelo, metric_value):
    st.success(f"✅ Modelo treinado com sucesso!")
    st.write(f"📈 Melhor modelo: `{modelo}` com métrica `{metric_value}`")

def mostrar_info(texto):
    st.info(texto)
