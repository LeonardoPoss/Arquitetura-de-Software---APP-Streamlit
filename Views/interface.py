import streamlit as st

def mostrar_titulo():
    st.title("App com MVC no Streamlit")

def mostrar_dados(df):
    st.subheader("📊 Dados Carregados:")
    st.dataframe(df)