# Controllers/SentimentController.py
from Models.Service.SentimentService import SentimentService
from Models.Service.ModelDBService import ModelDBService
import os

class SentimentController:
    def __init__(self):
        self.model_db = ModelDBService()

    def carregar_modelo(self, nome_modelo="modelo_sentimento.pkl"):
        caminho = os.path.join("Models", "Treinados", nome_modelo)
        caminho_baixado = self.model_db.carregar_modelo(nome_modelo, caminho)
        if caminho_baixado:
            return caminho_baixado
        return None

    def process_sentiment_analysis(self, df, text_col, label_col, nome_modelo="modelo_sentimento"):
        try:
            service = SentimentService(df, text_col, label_col)
            model = service.train_model()

            # Salvar modelo e retornar o nome/caminho
            caminho_salvo = service.save_model(model, filename=nome_modelo)
            return os.path.basename(caminho_salvo)  # Ex: modelo_sentimento.pkl
        except Exception as e:
            print(f"Erro na análise de sentimentos: {e}")
            return None
