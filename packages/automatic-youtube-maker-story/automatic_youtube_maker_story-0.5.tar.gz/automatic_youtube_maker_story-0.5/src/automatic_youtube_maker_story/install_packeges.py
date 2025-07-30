import subprocess
import os
import requests
import sys
import git
import yaml
import json


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
   

def pipInstallIndex(path, name_venv, pacotes, index_url):
    def_venv = os.path.join(path, name_venv, 'Scripts', 'python.exe')
    # Executa o pip install com --index-url
    try:
        subprocess.run([def_venv, "-m", "pip", "install", "--index-url", index_url] + pacotes)
        print(f"✅ pip instal concluido: {pacotes}")
    except subprocess.CalledProcessError:
        print(f"❌ Erro instalar pacotes: {pacotes}.")
        raise

def pipInstallIndexProjeto(pacotes, index_url):
    # Executa o pip install com --index-url
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--index-url", index_url] + pacotes
        )
        print(f"✅ pip install concluído: {pacotes}")
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao instalar pacotes: {pacotes}.")
        raise

def pipInstall(path, name_venv, pacotes):
    def_venv = os.path.join(path, name_venv, 'Scripts', 'python.exe')
    # Executa o pip install com --index-url
    try:
        subprocess.run([def_venv, "-m", "pip", "install", "--upgrade" ] + pacotes)
        print(f"✅ pip instal concluido: {pacotes}")
    except subprocess.CalledProcessError:
        print(f"❌ Erro instalar pacotes: {pacotes}.")
        raise

def pipInstallProjeto( pacotes):
    # Executa o pip install com --index-url
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacotes])
        print(f"✅ pip instal concluido: {pacotes}")
    except subprocess.CalledProcessError:
        print(f"❌ Erro instalar pacotes: {pacotes}.")
        raise

def pipUninstallProjeto(pacotes):
    # Executa o pip install com --index-url
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", pacotes])
        print(f"✅ pip instal concluido: {pacotes}")
    except subprocess.CalledProcessError:
        print(f"❌ Erro instalar pacotes: {pacotes}.")
        raise


def pipInstallReq(path, name_venv):
    req_file=os.path.join(path, "ComfyUI","requirements.txt")

    def_venv = os.path.join(path, name_venv, 'Scripts', 'python.exe')
    # Executa o pip install com --index-url
    try:
        
        subprocess.run([def_venv, "-m", "pip", "install", "-r", req_file])
        print(f"✅ pip instal concluido: {path}")
    except subprocess.CalledProcessError:
        print(f"❌ Erro instalar pacotes: {path}.")
        raise



def criar_venv(caminho_venv, venv_name, python_selec="python313"):

    def_venv = os.path.join(caminho_venv, venv_name)

    if python_selec == "python313":
        python_exec="C:/Users/"+os.environ.get('USERNAME')+"/AppData/Local/Programs/Python/Python313/python.exe"
    if python_selec == "python312":
        python_exec="C:/Users/"+os.environ.get('USERNAME')+"/AppData/Local/Programs/Python/python312/python.exe"
    if python_selec == "python311":
        python_exec="C:/Users/"+os.environ.get('USERNAME')+"/AppData/Local/Programs/Python/Python311/python.exe"
    if python_selec == "python310":
        python_exec="C:/Users/"+os.environ.get('USERNAME')+"/AppData/Local/Programs/Python/Python310/python.exe"
    if python_selec == "python39":
        python_exec="C:/Users/"+os.environ.get('USERNAME')+"/AppData/Local/Programs/Python/Python39/python.exe"

        

    """Cria um ambiente virtual em um caminho específico usando uma versão do Python."""
    def_venv = os.path.abspath(def_venv)  # Garante que o caminho é absoluto
    
    try:
        print(f"{python_exec} -m venv {def_venv}")
        subprocess.run([python_exec, "-m", "venv", def_venv], check=True)
        print(f"✅ Ambiente virtual criado em: {def_venv}")
    except subprocess.CalledProcessError:
        print(f"❌ Não Localizado python: {python_exec}")
        print(f"❌ Erro ao criar a venv. Verifique se {python_exec} está instalado.")
        raise

def cudaKIT126(path, filename=None):
        
    if os.path.isdir(r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6'):
        print(f'O diretório C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.6 existe.')
    else:
        print(f'O diretório C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.6 não existe. Instalando CUDA 12.6')
        url = "https://developer.download.nvidia.com/compute/cuda/12.6.0/local_installers/cuda_12.6.0_560.76_windows.exe"  # Substitua pela URL real
        print("Chegou", path)
        if filename is None:
            filename = url.split("/")[-1]  # Usa o nome do arquivo da URL se não for fornecido
        print("Chegou", path)
        file_path = os.path.join(path, filename)
        
        response = requests.get(url, stream=True)
        print(f"Baixando: {filename}")
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"✅ Arquivo salvo em: {file_path}")
            if file_path.endswith(".exe"):
                print(f"Executando {file_path}...")
                subprocess.run(file_path, shell=True)
                print(f"✅ Processo finalizado {file_path}...")
            else:
                print(f"❌ Erro ao executar arquivo! Não encontrado {filename}")
                raise
            # Deletar o arquivo
            try:
                os.remove(file_path)
                print(f"✅ Arquivo {file_path} deletado com sucesso.")
            except FileNotFoundError:
                print(f"❌ O arquivo {file_path} não foi encontrado.")
                raise
            except PermissionError:
                print(f"❌ Permissão negada para deletar o arquivo {file_path}.")
                raise
            except Exception as e:
                print(f"❌ Ocorreu um erro: {e}")
                raise
        else:
            print("❌ Erro ao baixar o arquivo.")
            raise

def set_env_variable(name, value):
    """
    Define uma variável de ambiente permanentemente no Windows utilizando o PowerShell como administrador.

    Parâmetros:
    name (str): Nome da variável de ambiente.
    value (str): Valor a ser atribuído à variável de ambiente.

    A função tenta definir a variável tanto no escopo 'Machine' (global).
    """
    for i in ['Machine']:
        command = f"[Environment]::SetEnvironmentVariable('{name}', '{value}', '{i}')"
        powershell_cmd = f'Start-Process powershell -ArgumentList \"{command}\" -Verb RunAs'
        
        print(powershell_cmd)
        try:
            subprocess.run( ["powershell", "-Command", powershell_cmd], shell=True, check=True)
            print(f"✔ Variável de ambiente {name} definida como {value} (Requer reinício para aplicar).")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao definir {name}: {e}")

def cudaKIT121(path):
        
    if os.path.isdir(r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1'):
        print(f'O diretório C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.1 existe.')
    else:
        print(f'O diretório C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.1 não existe. Instalando CUDA 12.1')
        url = "https://developer.download.nvidia.com/compute/cuda/12.1.1/local_installers/cuda_12.1.1_531.14_windows.exe"  # Substitua pela URL real
        
        if filename is None:
            filename = url.split("/")[-1]  # Usa o nome do arquivo da URL se não for fornecido
        
        file_path = os.path.join(path, filename)
        
        response = requests.get(url, stream=True)
        print(f"Baixando: {filename}")
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"✅ Arquivo salvo em: {file_path}")
            if file_path.endswith(".exe"):
                print(f"Executando {file_path}...")
                subprocess.run(file_path, shell=True)
                set_env_variable("CUDA_HOME", r"C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.1")
                set_env_variable("CUDA_PATH", r"C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.1")
                print(f"✅ Processo finalizado {file_path}...")
            else:
                print(f"❌ Erro ao executar arquivo! Não encontrado {filename}")
                raise
            # Deletar o arquivo
            try:
                os.remove(file_path)
                print(f"✅ Arquivo {file_path} deletado com sucesso.")
            except FileNotFoundError:
                print(f"❌ O arquivo {file_path} não foi encontrado.")
                raise
            except PermissionError:
                print(f"❌ Permissão negada para deletar o arquivo {file_path}.")
                raise
            except Exception as e:
                print(f"❌ Ocorreu um erro: {e}")
                raise
        else:
            print("❌ Erro ao baixar o arquivo.")
            raise

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
    try:
        os.makedirs(path_comfyUI, exist_ok=True)  
        print(f"✅ Criando pasta em: {path_comfyUI}")
        try:
            cudaKIT126(path_comfyUI)
            print(f"✅ CUDA 12.6 Configurado")

            try:
                criar_venv(path_comfyUI, name_venv, "python312")  # Substitua "python3.10" pela versão desejada
                # URL do repositório a ser clonado
                repo_url = "https://github.com/comfyanonymous/ComfyUI.git"
                

                try:                

                    pacotes =["torch", "torchvision", "torchaudio"]
                    index = "https://download.pytorch.org/whl/nightly/cu128"
                    pipInstallIndex(path_comfyUI,name_venv,pacotes,index)

                    try:
                        # Clonar o repositório

                        git.Repo.clone_from(repo_url,os.path.join(path_comfyUI, 'ComfyUI'))
                        print(f"✅ Repositório clonado em: {path_comfyUI}")
                        try:
                            pipInstallReq(path_comfyUI,name_venv)
                            return True
                        except:
                            return False

                    except subprocess.CalledProcessError:
                        print(f"❌ Erro ao clonar repositorio.")
                        raise

                except subprocess.CalledProcessError:
                    print(f"❌ Erro ao instalar pacotes: {pacotes}.")
                    raise
                



                
                    

                except:
                    print(f"❌ Erro ao clonar repositorio. Verifique se conexao com a internet, ou o caminho  {path_comfyUI} para instalação.")
                    raise
            except:
                print(f"❌ Erro ao criar a venv. Erro Fatal.")
                raise
        except:
                print(f"❌ Erro ao configurar Cuda 12.6.")
                raise
    except:
        print(f"❌ Erro ao criar ao criar pasta no caminho {path_comfyUI}.")
        return False

def addNationXTTs(path_root):
    path_rest = os.path.join(path_root, 'SOURCE')

    pipUninstallProjeto('narration-xtts2')

    pipUninstallProjeto('deepspeed')

    try:
        cudaKIT121(path_rest)
        print(f"✅ CUDA 12.1! Configurado|")

    except:
        print(f"❌ Erro ao configurar CUDA 12.1.")
        raise

    



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
    path_youtube_video =   input("[Youtube][Editor] Passe o caminho de input das referencias de voz:  ")
    CLIENT_SECRETS_FILE =   input("[Youtube] Passe o caminho da chave secreta de API google SERVICE OAUTH2.0:  ")

    config_data = {"path_root": add_trailing_slash(path_root), "path_base_comfy": add_trailing_slash(path_base),
                    "historic_history": historic_history, "path_video":  add_trailing_slash(path_video_out),
                    "path_video_out": add_trailing_slash(path_video_out), "path_history": add_trailing_slash(path_history),
                   "path_audio": add_trailing_slash(path_audio),"path_FX": add_trailing_slash(path_FX),"path_model": add_trailing_slash(path_model)
                   ,"path_ref": add_trailing_slash(path_ref),"path_youtube_video": add_trailing_slash(path_youtube_video), "CLIENT_SECRETS_FILE": CLIENT_SECRETS_FILE}
    salvar_json(config_data)
    

def start():
    configPaths()
    PATHS = config_call()
    path_root = PATHS["path_root"]

    print("Adicionando ComfyUI :")

    if addComfyUI(path_root):
        
        print(f"✅ ✅ ✅ COMFYUI instalado com sucesso ✅ ✅ ✅ ")
        print("Adicionando Narration-xtts2 story-children-gemma3 story-children-video-maker :")

        if addNationXTTs(path_root):
            
            print(f"✅ ✅ ✅ Narration-xtts2 story-children-gemma3 story-children-video-maker instalado com sucesso ✅ ✅ ✅ ")
        else:
            doc1 = "https://pypi.org/project/narration-xtts2/"
            doc2 = "https://pypi.org/project/story-children-gemma3/"
            doc3 = "https://pypi.org/project/story-children-video-maker/"
            print(f"❌ ❌ ❌ Narration-xtts2 story-children-gemma3 story-children-video-maker Falhou, veja documentação: {doc1}, {doc2}, {doc3}  ❌ ❌ ❌ ")    




    else:
        doc = "https://github.com/comfyanonymous/ComfyUI?tab=readme-ov-file#installing"
        print(f"❌ ❌ ❌ COMFYUI Falhou, veja documentação: {doc}  ❌ ❌ ❌ ")


    

    
if __name__ == "__main__":
    start()
    


    


    