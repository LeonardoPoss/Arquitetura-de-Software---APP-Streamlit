import os
import streamlit as st
import pandas as pd

from Models.Logger.Logging import setup_logging
from Models.Service.profiling import Profiling
from Controllers.Downloader import KaggleDownloader
from Models.Service.Archive_Selector import escolher_dataset_streamlit
from Models.Service.Trainer import PyCaretTrainer

logger = setup_logging()

def main():
    st.set_page_config(page_title="APP de Ciência de Dados", layout="wide")
    st.title("📊 Plataforma de Exploração e Treinamento de Dados")

    menu = st.sidebar.selectbox("Selecione uma opção", [
        "Início", 
        "Baixar Dataset (Kaggle)", 
        "Visualizar com D-Tale", 
        "Gerar Profiling (YData)", 
        "Treinar Modelo (PyCaret)"
    ])

    if menu == "Início":
        st.write("Bem-vindo! Escolha uma opção no menu lateral.")

    elif menu == "Baixar Dataset (Kaggle)":
        st.subheader("⬇️ Download do Dataset via Kaggle API")
        dataset_nome = st.text_input("Digite o nome do dataset (formato: user/dataset)")
        if st.button("Baixar Dataset"):
            if dataset_nome:
                API = KaggleDownloader(dataset_nome)
                if API:
                    st.success("✅ Autenticação realizada com sucesso.")
                    KaggleDownloader.verificar_e_baixar_dataset(API)
                else:
                    st.error("❌ Falha na autenticação do Kaggle.")
            else:
                st.warning("⚠️ Digite o nome do dataset corretamente.")

    elif menu == "Visualizar com D-Tale":
        st.subheader("📊 Visualização interativa com D-Tale")
        caminho = escolher_dataset_streamlit()
        if caminho:
            try:
                df = pd.read_csv(caminho)
                nome = os.path.basename(caminho)
                profiling = Profiling(nome, df)
                profiling.generate_dtale()
                st.success("✅ D-Tale aberto no navegador.")
            except Exception as e:
                st.error(f"Erro ao abrir com D-Tale: {e}")

    elif menu == "Gerar Profiling (YData)":
        st.subheader("📈 Gerar Relatório com YData Profiling")
        caminho = escolher_dataset_streamlit()
        if caminho:
            try:
                df = pd.read_csv(caminho)
                nome = os.path.basename(caminho)
                profiling = Profiling(nome, df)
                profiling.generate_ydata()
                st.success("✅ Relatório gerado.")
            except Exception as e:
                st.error(f"Erro ao gerar relatório: {e}")

    elif menu == "Treinar Modelo (PyCaret)":
        st.subheader("🤖 Treinar Modelo com PyCaret")
        caminho = escolher_dataset_streamlit()
        if caminho:
            try:
                df = pd.read_csv(caminho)
                colunas = df.columns.tolist()
                target = st.selectbox("Selecione a variável target", colunas)
                task_type = st.selectbox("Tipo de tarefa", ["classification", "regression", "clustering"])
                if st.button("Treinar modelo"):
                    trainer = PyCaretTrainer()
                    modelo = trainer.train_model(df, target, task_type)
                    st.success(f"✅ Modelo treinado com sucesso: {modelo}")
            except Exception as e:
                st.error(f"Erro no treinamento: {e}")

if __name__ == "__main__":
    main()
