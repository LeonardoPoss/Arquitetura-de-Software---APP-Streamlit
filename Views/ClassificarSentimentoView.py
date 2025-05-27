import os
import streamlit as st
import pandas as pd
from pycaret.classification import load_model, predict_model
from Models.Service.ModelDBService import ModelDBService

def classificar_sentimento_view():
    st.subheader("🧠 Classificação de Sentimentos")

    # Instancia o serviço DB
    db_service = ModelDBService()

    # Lista modelos disponíveis na pasta local
    pasta_treinados = os.path.join("Models", "Treinados")
    modelos_local = [f for f in os.listdir(pasta_treinados) if f.endswith(".pkl")] if os.path.exists(pasta_treinados) else []

    # Lista modelos disponíveis no banco (nomes)
    modelos_db = db_service.listar_modelos()

    modo_carregamento = st.radio("Selecionar modelo de:", ["Pasta local", "Banco de dados"])

    modelo_selecionado = None

    if modo_carregamento == "Pasta local":
        if not modelos_local:
            st.warning("Nenhum modelo encontrado na pasta local.")
            return
        modelo_file = st.selectbox("Escolha o modelo:", modelos_local)
        if modelo_file:
            # REMOVE a extensão .pkl para passar ao load_model
            nome_modelo_sem_ext = os.path.splitext(modelo_file)[0]
            caminho_modelo = os.path.join(pasta_treinados, nome_modelo_sem_ext)
            modelo_selecionado = load_model(caminho_modelo)
    else:
        if not modelos_db:
            st.warning("Nenhum modelo encontrado no banco de dados.")
            return
        modelo_nome = st.selectbox("Escolha o modelo salvo no banco:", modelos_db)
        if modelo_nome:
            modelo_selecionado = db_service.carregar_modelo(modelo_nome)

    if modelo_selecionado is not None:
        texto_input = st.text_area("Digite o texto para classificar o sentimento:")

        if st.button("Classificar"):
            if not texto_input.strip():
                st.warning("Por favor, insira um texto para classificar.")
                return

            # Criar DataFrame para a predição
            df_input = pd.DataFrame({"text": [texto_input]})

            # Prever usando pycaret predict_model
            pred = predict_model(modelo_selecionado, data=df_input)

            mapa_labels = {
                0: "Neutro",
                1: "Positivo",
                2: "Nostálgico",
                3: "Negativo",
                4: "Confuso",
                5: "Engraçado"
            }

            # Obtenção da predição
            if 'Label' in pred.columns:
                resultado = pred.loc[0, 'Label']
            elif 'prediction_label' in pred.columns:
                resultado = pred.loc[0, 'prediction_label']
            else:
                resultado = pred.loc[0, pred.columns[-1]]

            # Aplicar mapeamento, se possível
            resultado_legivel = mapa_labels.get(resultado, resultado)

            st.markdown(f"**Resultado da classificação:** {resultado_legivel}")

