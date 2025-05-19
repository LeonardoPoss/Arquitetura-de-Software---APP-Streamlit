import os
import streamlit as st

def escolher_dataset_streamlit(pasta=None):
    # Se nenhum caminho for passado, usa o padrão
    if pasta is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        pasta = os.path.abspath(os.path.join(base_dir, '..', 'Dataset'))

    # Lista arquivos com extensões válidas
    extensoes_validas = {".csv", ".json", ".xlsx"}
    try:
        arquivos = [
            f for f in os.listdir(pasta)
            if os.path.isfile(os.path.join(pasta, f))
            and os.path.splitext(f)[1] in extensoes_validas
        ]
    except FileNotFoundError:
        st.error(f"❌ A pasta especificada não foi encontrada: `{pasta}`")
        return None

    if not arquivos:
        st.warning("❌ Nenhum dataset encontrado na pasta.")
        return None

    st.subheader("📂 Selecione um dataset")
    dataset_escolhido = st.selectbox("Escolha um arquivo:", arquivos)

    if dataset_escolhido:
        caminho_completo = os.path.join(pasta, dataset_escolhido)
        st.success(f"✅ Dataset escolhido: {dataset_escolhido}")
        return caminho_completo

    return None
