import sqlite3
import os
from pycaret.classification import load_model

class ModelDBService:
    def __init__(self, db_path="Models/modelos.db"):
        self.db_path = db_path
        self._criar_tabela()

    def _criar_tabela(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS modelos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_modelo TEXT UNIQUE,
                    arquivo BLOB
                )
            ''')

    def salvar_modelo(self, nome_modelo, caminho_arquivo):
        with open(caminho_arquivo, "rb") as f:
            blob = f.read()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO modelos (nome_modelo, arquivo)
                VALUES (?, ?)
            ''', (nome_modelo, blob))
            conn.commit()

    def carregar_modelo(self, nome_modelo):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT arquivo FROM modelos WHERE nome_modelo = ?', (nome_modelo,))
            row = cursor.fetchone()
            if row is None:
                raise FileNotFoundError(f"Modelo {nome_modelo} não encontrado no banco de dados.")
            blob = row[0]

        nome_sem_ext = os.path.splitext(nome_modelo)[0]
        temp_path = os.path.join("Models", "Treinados", f"temp_{nome_sem_ext}")  # sem extensão .pkl

        with open(temp_path + ".pkl", "wb") as f:  # salva com .pkl de verdade no disco
            f.write(blob)

        model = load_model(temp_path)  # passa sem .pkl para load_model()

        os.remove(temp_path + ".pkl")  # remove o arquivo .pkl real

        return model

    def listar_modelos(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT nome_modelo FROM modelos")  # Corrigido nome da coluna
            resultados = cursor.fetchall()
            modelos = [row[0] for row in resultados]
        return modelos
