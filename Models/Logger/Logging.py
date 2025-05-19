import os 
import logging 

def setup_logging():
    """ Configura o sistema de logs para serem salvos em 'Logs' """
    log_dir = os.path.join(os.path.dirname(__file__), "..","Logs")
    os.makedirs(log_dir, exist_ok=True)  # Garante que a pasta exista

    log_file = os.path.join(log_dir, "Logs.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="a", encoding="utf-8"),  # Salva em arquivo
            logging.StreamHandler()  # Exibe no console
        ]
    )
    return logging.getLogger("Logs")