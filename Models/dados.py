import pandas as pd

def carregar_dados():
    # Exemplo simples com dataframe
    data = {
        "Nome": ["Ana", "Bruno", "Carlos"],
        "Idade": [23, 35, 45],
        "Cidade": ["SP", "RJ", "BH"]
    }
    df = pd.DataFrame(data)
    return df