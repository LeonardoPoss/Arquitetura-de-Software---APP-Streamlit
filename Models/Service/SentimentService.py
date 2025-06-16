import os
import pandas as pd
from pycaret.classification import setup, compare_models, save_model, pull
from Models.Service.ModelDBService import ModelDBService

class SentimentService:
    def __init__(self, df: pd.DataFrame, text_col: str, label_col: str):
        self.df = df
        self.text_col = text_col
        self.label_col = label_col
        self.model_db = ModelDBService()  # inicializa o serviço do DB

    def preprocess(self):
        # Seleciona colunas relevantes e remove nulos
        df_processado = self.df[[self.text_col, self.label_col]].dropna()
        df_processado.columns = ['text', 'target']
        return df_processado

    def train_model(self):
        df_processado = self.preprocess()
        clf_setup = setup(data=df_processado, target='target', session_id=123, verbose=False, html=False)
        best_model = compare_models()
        return best_model

    def save_model(self, model, filename="modelo_sentimento"):
        folder = os.path.join("Models", "Treinados")
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)

        # Salva o modelo no disco (sem duplicar extensão)
        save_model(model, path)

        # Adiciona .pkl para o nome do arquivo salvo
        caminho_completo = path + ".pkl"

        # Salva no banco
        self.model_db.salvar_modelo(nome_modelo=filename + ".pkl", caminho_arquivo=caminho_completo)

        return caminho_completo

    def load_model(self, filename="modelo_sentimento.pkl"):
        return self.model_db.carregar_modelo(filename)