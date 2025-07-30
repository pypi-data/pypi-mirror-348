import subprocess
import os
import requests
import sys
import git # type: ignore
import yaml
import json
from shutil import which
import venv
import platform
import glob



print(git.__version__)


def config_call():
    print("Carregando configs!")

    # Obtém o diretório do script atual
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define o caminho para salvar: uma pasta acima do script e dentro de "config/"
    path_config = os.path.join(script_dir, "config")

    file_path = os.path.join(path_config, "config.json")

    if os.path.exists(file_path) :
        # Lê o JSON existente
        with open(file_path, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    else:
        print("Erro config não existe")


def add_trailing_slash(path):
    """
    Adiciona o separador de diretórios correto (barra ou barra invertida) ao final do caminho, se não houver.
    """
    if not path.endswith(os.sep):
        return path + os.sep
    return path
    

def get_python_venv(path, name_venv):
    if platform.system() == "Windows":
        return os.path.join(path, name_venv, 'Scripts', 'python.exe')
    else:
        return os.path.join(path, name_venv, 'bin', 'python')


def pipInstallIndex(path, name_venv, pacotes, index_url):
    def_venv = get_python_venv(path, name_venv)
    try:
        subprocess.run([def_venv, "-m", "pip", "install", "--index-url", index_url] + pacotes, check=True)
        print(f"✅ pip install concluído: {pacotes}")
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao instalar pacotes: {pacotes}.")
        raise


def pipInstallIndexProjeto(pacotes, index_url):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--index-url", index_url] + pacotes)
        print(f"✅ pip install concluído: {pacotes}")
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao instalar pacotes: {pacotes}.")
        raise


def pipInstall(path, name_venv, pacotes):
    def_venv = get_python_venv(path, name_venv)
    try:
        subprocess.run([def_venv, "-m", "pip", "install", "--upgrade"] + pacotes, check=True)
        print(f"✅ pip install concluído: {pacotes}")
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao instalar pacotes: {pacotes}.")
        raise


def pipInstallProjeto(pacotes):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install" ,pacotes])
        print(f"✅ pip install concluído: {pacotes}")
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao instalar pacotes: {pacotes}.")
        raise


def pipUninstallProjeto(pacotes):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", pacotes])
        print(f"✅ pip uninstall concluído: {pacotes}")
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao desinstalar pacotes: {pacotes}.")
        raise


def pipInstallReq(path, name_venv):
    req_file = os.path.join(path, "ComfyUI", "requirements.txt")
    def_venv = get_python_venv(path, name_venv)
    try:
        subprocess.run([def_venv, "-m", "pip", "install", "-r", req_file], check=True)
        print(f"✅ pip install concluído: {req_file}")
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao instalar pacotes do arquivo: {req_file}.")
        raise



def criar_venv(caminho_venv, venv_name, python_selec="python311"):
    def_venv = os.path.join(caminho_venv, venv_name)

    # Mapeia nomes amigáveis para comandos reais do sistema
    python_versions = {
        "python313": "python3.13",
        "python312": "python3.12",
        "python311": "python3.11",
        "python310": "python3.10",
        "python39":  "python3.9",
    }

    python_exec = python_versions.get(python_selec)

    if not python_exec or which(python_exec) is None:
        print(f"❌ Python '{python_selec}' não encontrado no sistema.")
        return

    def_venv = os.path.abspath(def_venv)

    try:
        print(f"{python_exec} -m venv {def_venv}")
        subprocess.run([python_exec, "-m", "venv", def_venv], check=True)
        print(f"✅ Ambiente virtual criado em: {def_venv}")
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao criar o ambiente virtual com {python_exec}")
        raise







def set_env_variable(name, value, shell_config_file="~/.bashrc"):
    shell_config_path = os.path.expanduser(shell_config_file)
    line = f'\nexport {name}="{value}"\n'

    with open(shell_config_path, 'a') as f:
        f.write(line)
    print(f"Variável {name} adicionada a {shell_config_path}. Faça logout/login para aplicar.")


def instalar_cuda128_ubuntu2404():
    # Verifica se o pacote 'cuda-toolkit-12-8' já está instalado
    print("🔍 Verificando se o CUDA 12.8 já está instalado...")
    resultado_verificacao = subprocess.run(
        ["dpkg", "-l", "cuda-toolkit-12-8"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if resultado_verificacao.returncode == 0:
        print("✅ CUDA 12.8 já está instalado. Pulando a instalação.")
        return
    keyring_files = glob.glob("/var/cuda-repo-ubuntu2404-12-8-local/cuda-*-keyring.gpg")
    comandos = [
        # Baixa o arquivo .pin
        ["wget", "https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-ubuntu2404.pin"],

        # Move o .pin para o local correto
        ["sudo", "mv", "cuda-ubuntu2404.pin", "/etc/apt/preferences.d/cuda-repository-pin-600"],

        # Baixa o instalador .deb do repositório local
        ["wget", "https://developer.download.nvidia.com/compute/cuda/12.8.0/local_installers/cuda-repo-ubuntu2404-12-8-local_12.8.0-570.86.10-1_amd64.deb"],

        # Instala o repositório local
        ["sudo", "dpkg", "-i", "cuda-repo-ubuntu2404-12-8-local_12.8.0-570.86.10-1_amd64.deb"],

        # Copia a chave GPG
        ["sudo", "cp", keyring_files[0] ,"/usr/share/keyrings/"],

        # Atualiza os pacotes
        ["sudo", "apt-get", "update"],

        # Instala o CUDA Toolkit
        ["sudo", "apt-get", "-y", "install", "cuda-toolkit-12-8"],

        # Limpa o instalador .deb
        ["sudo", "rm", "cuda-repo-ubuntu2404-12-8-local_12.8.0-570.86.10-1_amd64.deb"]
    ]

    for comando in comandos:
        print(f"\nExecutando: {' '.join(comando)}")
        resultado = subprocess.run(comando)
        if resultado.returncode != 0:
            print(resultado.returncode)
            print(resultado.stderr)
            print(f"❌ Erro ao executar: {' '.join(comando)}")
            break



def instalar_cuda121_ubuntu2404():
    # Verifica se o pacote 'cuda-toolkit-12-1' já está instalado
    print("🔍 Verificando se o CUDA 12.1 já está instalado...")
    resultado_verificacao = subprocess.run(
        ["dpkg", "-l", "cuda-toolkit-12-1"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if resultado_verificacao.returncode == 0:
        print("✅ CUDA 12.1 já está instalado. Pulando a instalação.")
        return
    keyring_files = glob.glob("/var/cuda-repo-ubuntu2204-12-1-local/cuda-*-keyring.gpg")
    comandos = [
        # Baixa o arquivo .pin
        ["wget", "https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin"],

        # Move o .pin para o local correto
        ["sudo", "mv", "cuda-ubuntu2204.pin", "/etc/apt/preferences.d/cuda-repository-pin-600"],

        # Baixa o instalador .deb do repositório local
        ["wget", "https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda-repo-ubuntu2204-12-1-local_12.1.0-530.30.02-1_amd64.deb"],

        # Instala o repositório local
        ["sudo", "dpkg", "-i", "cuda-repo-ubuntu2204-12-1-local_12.1.0-530.30.02-1_amd64.deb"],

        # Copia a chave GPG
        ["sudo", "cp", keyring_files[0], "/usr/share/keyrings/"],

        # Atualiza os pacotes
        ["sudo", "apt-get", "update"],

        # Instala o CUDA Toolkit
        ["sudo", "apt-get", "-y", "install", "cuda-toolkit-12-1"],
        
        # limpar o instalador .deb do repositório local
        ["sudo", "rm", "cuda-repo-ubuntu2204-12-1-local_12.1.0-530.30.02-1_amd64.deb"]
    ]

    for comando in comandos:
        print(f"\nExecutando: {' '.join(comando)}")
        resultado = subprocess.run(comando)
        if resultado.returncode != 0:
            print(f"❌ Erro ao executar: {' '.join(comando)}")
            print(resultado.returncode)
            print(resultado.stderr)
            break
            


def literal_str_presenter(dumper, data):
    # Se a string contiver quebra de linha, forçamos o estilo literal '|'
    if "\n" in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

def salveYamlComfy(path_compfy,path_base):
    # Dados que você deseja salvar no arquivo YAML
    # Adiciona o representador customizado para strings
    yaml.add_representer(str, literal_str_presenter)
    
    data = {
    'comfyui': {
            'base_path': path_base,
            'is_default': True,
            'checkpoints': 'models/checkpoints/',
            'clip': 'models/clip/',
            'clip_vision': 'models/clip_vision/',
            'configs': 'models/configs/',
            'controlnet': 'models/controlnet/',
            'diffusion_models': '''models/diffusion_models
models/unet''',
            'embeddings': 'models/embeddings/',
            'loras': 'models/loras/',
            'upscale_models': 'models/upscale_models/',
            'vae': 'models/vae/'
        }
    }


    # Caminho onde o arquivo .yaml será salvo
    yaml_file = os.path.join(path_compfy, "ComfyUI",  'extra_model_paths.yaml')

    # Salvar o dicionário Python como um arquivo YAML
    with open(yaml_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

    print(f'Arquivo {yaml_file} foi salvo com sucesso!')

def startSeverComfyUI(path, name_venv, path_out):
    script_main=os.path.join(path, "ComfyUI","main.py")

    def_venv = os.path.join(path, name_venv, 'Scripts', 'python.exe')
    # Executa o pip install com --index-url
    try:
        
        subprocess.run([def_venv, script_main, "--output-directory", path_out])
        print(f"✅ Servidor iniciado salvando no caminho: {path_out}")
        print(f"Para finalizar teste CRTL+C")
    except subprocess.CalledProcessError:
        print(f"❌ Falha ao iniciar server")
        raise




def addComfyUI(path_root):
    path_comfyUI = os.path.join(path_root, 'SOURCE')
    name_venv = "venv_comfy"
    repo_url = "https://github.com/comfyanonymous/ComfyUI.git"

    try:
        os.makedirs(path_comfyUI, exist_ok=True)
        print(f"✅ Criando pasta em: {path_comfyUI}")
    except Exception as e:
        print(f"❌ Erro ao criar pasta {path_comfyUI}: {e}")
        return False
    
    try:
        instalar_cuda128_ubuntu2404()
        print(f"✅ CUDA 12.8 Configurado")
    except Exception as e:
        print(f"❌ Erro ao configurar CUDA 12.8: {e}")
        return False
    
    

    try:
        criar_venv(path_comfyUI, name_venv, "python312")
    except Exception as e:
        print(f"❌ Erro ao criar venv: {e}")
        return False

    pacotes = ["torch", "torchvision", "torchaudio"]
    index = "https://download.pytorch.org/whl/nightly/cu128"

    try:
        pipInstallIndex(path_comfyUI, name_venv, pacotes, index)
    except Exception as e:
        print(f"❌ Erro ao instalar pacotes {pacotes}: {e}")
        return False

    try:
        git.Repo.clone_from(repo_url, os.path.join(path_comfyUI, 'ComfyUI'))
        print(f"✅ Repositório clonado em: {path_comfyUI}")
    except Exception as e:
        print(f"❌ Erro ao clonar repositório: {e}")
        return False

    try:
        pipInstallReq(path_comfyUI, name_venv)
    except Exception as e:
        print(f"❌ Erro ao instalar requisitos: {e}")
        return False

    return True


def addNationXTTs(path_root):

    
    pipInstallProjeto('narration-xtts2')
    pipUninstallProjeto('narration-xtts2')
    
    try:                
        # torch                   2.3.1+cu121  Tensors and Dynamic neural networks in Python with strong GPU acceleration
        # torchaudio              2.3.1+cu121  An audio package for PyTorch
        # torchvision             0.18.1+cu121 image and video datasets and models for torch deep learning

        pacotes =["torch==2.3.1", "torchvision==0.18.1", "torchaudio==2.3.1"]
        index = "https://download.pytorch.org/whl/cu121"
        pipInstallIndexProjeto(pacotes,index)

    except subprocess.CalledProcessError:
        print(f"❌ Erro ao instalar pacotes: {pacotes}.")
        raise

    pipInstallProjeto('narration-xtts2')
    pipUninstallProjeto('deepspeed')
    pipInstallProjeto('deepspeed==0.15')

    return True
            



        




    

def salvar_json(dados, filename="config.json"):
    """
    Salva um dicionário em formato JSON em um arquivo dentro do diretório 'config'.

    Parâmetros:
    dados (dict): Dados a serem salvos no arquivo JSON.
    filename (str): Nome do arquivo JSON. Padrão é 'config.json'.

    O arquivo será salvo em um diretório 'config' localizado no nível acima do diretório do script atual.
    """
    # Obtém o diretório do script atual
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define o caminho para salvar: uma pasta acima do script e dentro de "config/"
    save_dir = os.path.join(script_dir, "config")

    # Garante que a pasta "config" existe
    os.makedirs(save_dir, exist_ok=True)

    # Caminho completo do arquivo JSON
    file_path = os.path.join(save_dir, filename)

    # Salva o JSON
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(dados, json_file, indent=4, ensure_ascii=False)
    
    print(f"JSON salvo em: {file_path}")


def configPaths():
    path_root = input("Root projeto: ")
    path_base = input("diretorio output do ComfyUI: ")
    historic_history = input("[Todos] Passe o arquivo de controle conteudo .json: ")
    path_video_out = input("[Video] Passe o caminho de output dos videos do comfy:  ")
    path_history = input("[Todos] Passe o caminho de output das history:  ")
    path_audio = input("[Narration][Editor] Passe o caminho de output das Narrações:  ")
    path_FX = input("[Editor] Passe o caminho de input dos efeitos especiais FX:  ")
    path_model = input("[Narration] Passe o caminho dos modelos de XTTS:  ")
    path_ref =   input("[Narration] Passe o caminho de input das referencias de voz:  ")
    path_youtube_video =   input("[Youtube][Editor] Output dos videos editados:  ")
    CLIENT_SECRETS_FILE =   input("[Youtube] Passe o caminho da chave secreta de API google SERVICE OAUTH2.0:  ")

    config_data = {"path_root": add_trailing_slash(path_root), "path_base_comfy": add_trailing_slash(path_base),
                    "historic_history": historic_history, "path_video":  add_trailing_slash(path_video_out),
                    "path_video_out": add_trailing_slash(path_video_out), "path_history": add_trailing_slash(path_history),
                   "path_audio": add_trailing_slash(path_audio),"path_FX": add_trailing_slash(path_FX),"path_model": add_trailing_slash(path_model)
                   ,"path_ref": add_trailing_slash(path_ref),"path_youtube_video": add_trailing_slash(path_youtube_video), "CLIENT_SECRETS_FILE": CLIENT_SECRETS_FILE}
    salvar_json(config_data)
    

def start():
    # configPaths()
    PATHS = config_call()
    path_root = PATHS["path_root"]

    
    
    if addNationXTTs(path_root):
            
        print(f"✅ ✅ ✅ Narration-xtts2 story-children-gemma3 story-children-video-maker instalado com sucesso ✅ ✅ ✅ ")
        print("Adicionando ComfyUI :")
        
        if addComfyUI(path_root):
        
            print(f"✅ ✅ ✅ COMFYUI instalado com sucesso ✅ ✅ ✅ ")
            print("Adicionando Narration-xtts2 story-children-gemma3 story-children-video-maker :")


        else:
            doc = "https://github.com/comfyanonymous/ComfyUI?tab=readme-ov-file#installing"
            print(f"❌ ❌ ❌ COMFYUI Falhou, veja documentação: {doc}  ❌ ❌ ❌ ")
    else:
        doc1 = "https://pypi.org/project/narration-xtts2/"
        doc2 = "https://pypi.org/project/story-children-gemma3/"
        doc3 = "https://pypi.org/project/story-children-video-maker/"
        print(f"❌ ❌ ❌ Narration-xtts2 story-children-gemma3 story-children-video-maker Falhou, veja documentação: {doc1}, {doc2}, {doc3}  ❌ ❌ ❌ ")    




    


    

    
if __name__ == "__main__":
    start()
    


    


    