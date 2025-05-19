import os
import pandas as pd
import streamlit as st
import dtale
from ydata_profiling import ProfileReport
from streamlit.components.v1 import html

class Profiling:
    def __init__(self, nome_arquivo: str, df: pd.DataFrame):
        self.nome_arquivo = nome_arquivo
        self.df = df

        # Define a pasta para os relatórios como 'Views'
        self.output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Views"))
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_dtale(self):
        """ Inicia D-Tale e retorna o link da instância para ser exibida no Streamlit """
        try:
            instancia = dtale.show(self.df, ignore_duplicate=True)
            url = instancia._main_url

            st.success(f"D-Tale iniciado para {self.nome_arquivo}")
            st.markdown(f"🔗 [Clique aqui para abrir o D-Tale]({url})")
            return url
        except Exception as e:
            st.error(f"Erro ao iniciar D-Tale: {e}")

    def generate_ydata(self, sample_frac: float = 0.01, min_rows: int = 500, random_state: int = 50):
        """ Gera relatório YData Profiling e exibe um iframe com o resultado """
        try:
            # Amostragem
            if len(self.df) > min_rows:
                dataset_amostrado = self.df.sample(frac=sample_frac, random_state=random_state)
            else:
                dataset_amostrado = self.df.copy()

            # Gera o relatório
            profile = ProfileReport(dataset_amostrado, explorative=True)
            output_path = os.path.join(self.output_dir, f"ydata_{self.nome_arquivo}.html")
            profile.to_file(output_path)
            html_output = profile.to_html()
            
            st.success("✅ Relatório YData gerado com sucesso!")
            st.markdown("### 🔍 Visualização interativa do relatório")
            html(html_output, height=1000, scrolling=True)

        except Exception as e:
            st.error(f"Erro ao gerar relatório YData: {e}")
