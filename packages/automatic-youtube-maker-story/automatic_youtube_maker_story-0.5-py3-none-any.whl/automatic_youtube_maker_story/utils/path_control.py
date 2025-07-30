
import os
import json

def config_paths(filename="config.json"):

    # Obtém o diretório do script atual
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define o caminho para salvar: uma pasta acima do script e dentro de "config/"
    save_dir = os.path.join(os.path.dirname(script_dir), "config")

    # Garante que a pasta "config" existe
    os.makedirs(save_dir, exist_ok=True)

    # Caminho completo do arquivo JSON
    file_path = os.path.join(save_dir, filename)

    # Lê o JSON existente
    with open(file_path, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)