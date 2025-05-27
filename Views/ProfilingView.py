# Views/ProfilingView.py

import streamlit as st
import pandas as pd
from streamlit.components.v1 import html
from Models.Service.ProfilingService import ProfilingService
from Models.Service.Archive_Selector import escolher_dataset_streamlit

def exibir_dtale_view():
    st.subheader("📊 Visualização interativa com D-Tale")
    caminho = escolher_dataset_streamlit()
    if caminho:
        nome = caminho.split("/")[-1]
        if st.button("✅ Confirmar e abrir com D-Tale"):
            try:
                df = pd.read_csv(caminho)
                profiler = ProfilingService(nome, df)
                url = profiler.iniciar_dtale()
                st.success(f"D-Tale iniciado para {nome}")
                st.markdown(f"🔗 [Clique aqui para abrir o D-Tale]({url})")
            except Exception as e:
                st.error(f"Erro ao abrir com D-Tale: {e}")

def exibir_ydata_view():
    st.subheader("📈 Gerar Relatório com YData Profiling")
    caminho = escolher_dataset_streamlit()
    if caminho:
        nome = caminho.split("/")[-1]
        if st.button("✅ Confirmar e gerar relatório YData"):
            try:
                df = pd.read_csv(caminho)
                profiler = ProfilingService(nome, df)
                df_amostrado = profiler.gerar_amostra()
                html_output = profiler.gerar_ydata_html(df_amostrado)

                st.success("✅ Relatório YData gerado com sucesso!")
                st.markdown("### 🔍 Visualização interativa do relatório")
                html(html_output, height=1000, scrolling=True)
            except Exception as e:
                st.error(f"Erro ao gerar relatório YData: {e}")
