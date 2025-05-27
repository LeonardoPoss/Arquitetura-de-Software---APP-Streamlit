import os
import streamlit as st
from Models.Service.ModelDBService import ModelDBService

def salvar_arquivos_no_banco_view():
    pasta_treinados = os.path.join("Models", "Treinados")
    if not os.path.exists(pasta_treinados):
        st.error("A pasta 'Models/Treinados' não existe.")
        return

    arquivos = [f for f in os.listdir(pasta_treinados) if os.path.isfile(os.path.join(pasta_treinados, f))]
    if not arquivos:
        st.info("Nenhum arquivo encontrado na pasta 'Models/Treinados'.")
        return

    st.subheader("📁 Arquivos em 'Models/Treinados'")
    checkboxes = {}
    for arquivo in arquivos:
        checkboxes[arquivo] = st.checkbox(arquivo)

    if st.button("💾 Salvar arquivos selecionados no banco"):
        selecionados = [f for f, checked in checkboxes.items() if checked]
        if not selecionados:
            st.warning("⚠️ Nenhum arquivo selecionado.")
            return

        db_service = ModelDBService()
        sucesso = []
        falha = []

        for arquivo in selecionados:
            caminho = os.path.join(pasta_treinados, arquivo)
            try:
                db_service.salvar_modelo(arquivo, caminho)
                sucesso.append(arquivo)
            except Exception as e:
                falha.append((arquivo, str(e)))

        if sucesso:
            st.success(f"✅ Arquivos salvos com sucesso: {', '.join(sucesso)}")
        if falha:
            for arquivo, erro in falha:
                st.error(f"❌ Erro ao salvar {arquivo}: {erro}")
