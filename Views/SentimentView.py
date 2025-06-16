import streamlit as st
import pandas as pd
from Controllers.SentimentController import SentimentController
from Models.Service.Archive_Selector import escolher_dataset_streamlit

def sentiment_analysis_view():
    st.subheader("🧠 Análise de Sentimentos com PyCaret")

    caminho = escolher_dataset_streamlit()
    if caminho:
        try:
            df = pd.read_csv(caminho)
            colunas = df.columns.tolist()

            text_col = st.selectbox("Selecione a coluna de texto", colunas)
            label_col = st.selectbox("Selecione a coluna de rótulo (sentimento)", colunas)

            if st.button("Executar Análise de Sentimentos"):
                controller = SentimentController()
                model = controller.process_sentiment_analysis(df, text_col, label_col)
                if model:
                    st.success(f"✅ Modelo treinado: {model}")
                else:
                    st.error("❌ Falha ao treinar o modelo")

        except Exception as e:
            st.error(f"Erro ao carregar o dataset: {e}")
    else:
        st.info("Por favor, selecione um dataset para continuar.")
