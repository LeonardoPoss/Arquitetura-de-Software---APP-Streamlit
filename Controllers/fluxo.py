from Models.dados import carregar_dados
from Views.interface import mostrar_titulo, mostrar_dados

def executar_app():
    mostrar_titulo()
    df = carregar_dados()
    mostrar_dados(df)