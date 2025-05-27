# Models/Service/ProfilingService.py

import os
import pandas as pd
from ydata_profiling import ProfileReport
import dtale

class ProfilingService:
    def __init__(self, nome_arquivo: str, df: pd.DataFrame):
        self.nome_arquivo = nome_arquivo
        self.df = df

        self.output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Views"))
        os.makedirs(self.output_dir, exist_ok=True)

    def gerar_amostra(self, sample_frac: float = 0.01, min_rows: int = 500, random_state: int = 50):
        if len(self.df) > min_rows:
            return self.df.sample(frac=sample_frac, random_state=random_state)
        return self.df.copy()

    def gerar_ydata_html(self, df_amostrado: pd.DataFrame):
        profile = ProfileReport(df_amostrado, explorative=True)
        output_path = os.path.join(self.output_dir, f"ydata_{self.nome_arquivo}.html")
        profile.to_file(output_path)
        return profile.to_html()

    def iniciar_dtale(self):
        instancia = dtale.show(self.df, ignore_duplicate=True)
        return instancia._main_url
