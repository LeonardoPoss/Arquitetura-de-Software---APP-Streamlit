import os
import streamlit as st
import pandas as pd

from Models.Logger.Logging import setup_logging
from Controllers.Downloader import KaggleDownloader
from Models.Service.Archive_Selector import escolher_dataset_streamlit
from Models.Service.Trainer import PyCaretTrainer
from Controllers.HuggingFaceDownloader import HuggingFaceDownloader
from Views.DownloadView import input_dataset_link, mostrar_mensagem
from Views.TrainView import selecionar_treinamento, mostrar_resultado_treinamento, mostrar_info
from Views.ProfilingView import exibir_dtale_view, exibir_ydata_view
from Views.SentimentView import sentiment_analysis_view
from Views.SalvarArquivosDBView import salvar_arquivos_no_banco_view
from Views.ClassificarSentimentoView import classificar_sentimento_view

logger = setup_logging()

def main():
    st.set_page_config(page_title="APP de Ciência de Dados", layout="wide")
    st.title("📊 Plataforma de Exploração e Treinamento de Dados")

    menu = st.sidebar.selectbox("Selecione uma opção", [
        "Início", 
        "Baixar Dataset (Link)", 
        "Visualizar com D-Tale", 
        "Gerar Profiling (YData)", 
        "Treinar Modelo (PyCaret)",
        "Análise de Sentimentos",
        "Salvamento Manual (DB)",
        "Classificador de Sentimento"
    ])

    if menu == "Início":
        st.write("Bem-vindo! Escolha uma opção no menu lateral.")

    elif menu == "Baixar Dataset (Link)":
        url, baixar = input_dataset_link()
        if baixar:
            if not url:
                mostrar_mensagem("aviso", "⚠️ Por favor, insira um link.")
                return
            
            if "kaggle.com" in url:
                try:
                    dataset_id = url.split("kaggle.com/datasets/")[-1].split("?")[0].strip("/")
                    downloader = KaggleDownloader(dataset_id)
                    downloader.verificar_e_baixar_dataset()
                    mostrar_mensagem("sucesso", "✅ Download do Kaggle finalizado.")
                except Exception as e:
                    mostrar_mensagem("erro", f"❌ Erro ao processar link do Kaggle: {e}")
            elif "huggingface.co" in url:
                try:
                    dataset_id = url.split("huggingface.co/datasets/")[-1].split("?")[0].strip("/")
                    hf_downloader = HuggingFaceDownloader(dataset_id)
                    hf_downloader.baixar_e_salvar()
                    mostrar_mensagem("sucesso", "✅ Download do Hugging Face finalizado.")
                except Exception as e:
                    mostrar_mensagem("erro", f"❌ Erro ao processar link do Hugging Face: {e}")
            else:
                mostrar_mensagem("erro", "❌ Link não reconhecido. Suporte apenas para Kaggle e Hugging Face.")

    elif menu == "Visualizar com D-Tale":
        exibir_dtale_view()

    elif menu == "Gerar Profiling (YData)":
        exibir_ydata_view()

    elif menu == "Treinar Modelo (PyCaret)":
        caminho = escolher_dataset_streamlit()
        df, nome_dataset, target, task_type, treinar = selecionar_treinamento(caminho)
        if treinar and df is not None:
            try:
                trainer = PyCaretTrainer()
                modelo, metric_value = trainer.train_model(df, target, task_type)
                mostrar_resultado_treinamento(nome_dataset, modelo, metric_value)
            except Exception as e:
                st.error(f"Erro no treinamento: {e}")
                
    elif menu == "Análise de Sentimentos":
        sentiment_analysis_view()
        
    elif menu == "Salvamento Manual (DB)":
        salvar_arquivos_no_banco_view()
        
    elif menu == "Classificador de Sentimento":
        classificar_sentimento_view()
        

if __name__ == "__main__":
    main()
