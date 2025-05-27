import streamlit as st

def input_dataset_link():
    st.subheader("⬇️ Baixar Dataset via Link")
    url = st.text_input("🔗 Insira o link do dataset (Kaggle ou Hugging Face)")
    baixar = st.button("Baixar")
    return url, baixar

def mostrar_mensagem(tipo, texto):
    if tipo == "erro":
        st.error(texto)
    elif tipo == "sucesso":
        st.success(texto)
    elif tipo == "aviso":
        st.warning(texto)
    elif tipo == "info":
        st.info(texto)
