from ollama import Client
import json
import os
import regex as re
from tqdm import tqdm
import platform
import unicodedata

if platform.system() == "Linux":
    
    
    import subprocess
    import os
    import signal
    import psutil

    # Variável global para guardar o processo do servidor
    ollama_process = None
        


    def start_ollama_server():
        global ollama_process
        ollama_process = subprocess.Popen(
            ["ollama", "run", "gemma3:27b"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )
        print("Servidor Ollama iniciado.")

    def stop_ollama_server():
        global ollama_process
        if ollama_process is None:
            # tenta matar processo externo caso esteja rodando
            for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    if "ollama" in proc.info["name"] and "run" in proc.info["cmdline"] and "gemma3:27b" in proc.info["cmdline"]:
                        print(f"Matar processo Ollama PID: {proc.pid}")
                        proc.kill()
                        print("Servidor Ollama parado.")
                        return
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            print("Nenhum processo Ollama encontrado.")
        else:
            os.killpg(os.getpgid(ollama_process.pid), signal.SIGTERM)
            ollama_process = None
            print("Servidor Ollama parado.")


def interfaceUtils():

    # Chamada config troca para teste direto

    # import utils
    # return utils.config_paths()

    return {
        "path_root": "/home/will/Documentos/Github/Contos-Magicos/",
    "path_base_comfy": "/media/will/illiam/Youtube/confyui/models/",
    "historic_history": "/media/will/illiam/Youtube/ContosMagicos/controle.json",
    "path_video": "/media/will/illiam/Youtube/confyui/comfyui_out/",
    "path_video_out": "/media/will/illiam/Youtube/confyui/comfyui_out/",
    "path_history": "/media/will/illiam/Youtube/ContosMagicos/History/",
    "path_audio": "/media/will/illiam/Youtube/ContosMagicos/Narration/audios/",
    "path_FX": "/media/will/illiam/Youtube/FX/",
    "path_model": "/media/will/illiam/Youtube/ContosMagicos/Narration/model/",
    "path_ref": "/media/will/illiam/Youtube/ContosMagicos/Narration/vozes/",
    "path_youtube_video": "/media/will/illiam/Youtube/ContosMagicos/youtube_video/",
    "CLIENT_SECRETS_FILE": ""
    }




def safeTextUnicodeYoutube(texto):
    # Substitui aspas duplas por uma string vazia
    texto_sem_aspas = texto.replace('"', '')
    # Substitui quebras de linha por uma string vazia
    texto_limpo = texto_sem_aspas.replace('\n', '')

    return texto_limpo

def safeTextUnicodeSpeak(texto):
    # Substitui caracteres que não sejam letras, vírgulas, pontos de interrogação, pontos de exclamação ou espaços
    return re.sub(r'[^\p{L},¡¿!? ]+', '', texto)

def safeTextUnicodeScene(texto):
    # Substitui caracteres que não sejam letras, vírgulas, pontos de interrogação, pontos de exclamação ou espaços
    return re.sub(r'[^\p{L},¡¿!? .:]+', '', texto)


def formatPromptYoutube(history, tema, licao):
    """
    Gera o prompt para criação de conteúdo para YouTube baseado na história infantil.

    Parâmetros:
        history (str): A história infantil completa.
        tema (str): O tema utilizado para gerar a história.
        licao (str): A lição ou moral da história.

    Retorna:
        str: Um prompt formatado que solicita a geração de título, descrição e tags 
             para o vídeo no YouTube, estruturado em JSON.
    """
    return "Considere a história infantil: "+ history +". Gerado pelo tema '"+ tema + "' com a lição da história '" + licao + """'
    Gere para o youtube:

    [title] Um ótimo título incrível para história, adicione também ícones e emojis  o inicio e final do titulo.
     
    [description] Também gere uma ótima descrição, se possível utilize alguns emojis .
    
    [tags] Gere ótimas tag/palavras chaves no formato "tag, tag, tag,..." para youtube, ou seja, apenas as palavras chaves separado por virgula com máximo de 400 caracteres, elabore para vídeo no YouTube, adicione ícones interessantes sobre o tema, hashtag na descrição.

    responda apenas em texto extritamente nesta estrutura JSON:

    {
        "title": "....",
        "tags": ["tag1","tag2",...],
        "description":"..."    

    }"""


def formatPromptNarracao(tema, licao):
    """
    Gera o prompt para criação de uma história infantil narrada.

    Parâmetros:
        tema (str): O tema da história.
        licao (str): A lição ou moral da história.

    Retorna:
        str: Um prompt formatado que solicita a geração de uma narração da história,
             com frases de aproximadamente 120 caracteres cada e cerca de 12 frases, 
             estruturado em JSON.
    """
    return """
    
    Gere uma história infantil com o tema " 
    
    
    """ + tema + """ 
    
    " com a lição da história " 
    
    
    """ + licao + """ 
    
    " . Quero o formato da seguinte forma:

    [narration] Narração frase a frase de aproximadamente 120 caracteres, e aproximadamente 12 frases.
    responda apenas como texto extritamente nesta estrutura JSON:

    {
        "narration":[ "frase1 ....", "frase2 ...", ...]

    }"""

def formatPromptDescriptionScenes(scene, history, person):
    """
    Gera um prompt claro e objetivo para descrever uma cena, adequado para modelos de geração de vídeo.

    Parâmetros:
        scene (str): Trecho específico da narração a ser representado.
        history (str): História completa, para contexto.
        person (str): Descrição do personagem principal, usada em todas as cenas.

    Retorna:
        str: Um prompt formatado com instruções claras para gerar uma descrição visual objetiva da cena.
    """
    return f"""
                Considere o seguinte trecho da história:

                Contexto geral: {history}

                Cena específica: "{scene}"

                Descreva a cena com base nas seguintes instruções:

                - Foque na ação principal do personagem, no local onde a cena ocorre e nos elementos visuais.
                - Evite figuras de linguagem, metáforas ou termos subjetivos como 'incrível', 'fantástico', etc.
                - Mencione o personagem principal, com esta descrição: {person}
                - Repita essa descrição do personagem sempre que ele estiver presente.
                - O resultado deve conter no máximo 400 caracteres.
                - NÃO inclua explicações, interpretações ou contexto narrativo.
                - NÃO use ponto final, ponto e virgula ou aspas.
                - NÃO use nomes de pessoas ou locais fictícios.
                - Utilize linguagem simples.
                - Evite linguagem figurativa, literária ou subjetiva.
                - Descreva apenas o que pode ser visto na cena: roupas, aparência, ações físicas, cores, objetos e cenário.
                - Conecte ações com vírgulas ou palavras simples como "enquanto", "depois", "em seguida".

                Formato da resposta:
                "Descrição da cena em linguagem direta e visual, com foco em personagens e ambiente."

                Apenas o texto da descrição, sem explicações ou formatação adicional.
                """


def formatPromptDescriptionPerson(history):
    """
    Gera um prompt para descrever visualmente o personagem principal da história (pessoa, animal ou objeto animado).

    Parâmetros:
        history (str): Texto completo da história, utilizado como base para identificar o personagem principal.

    Retorna:
        str: Um prompt formatado com instruções claras para gerar uma descrição visual objetiva e relevante para vídeo.
    """
    return f"""
            Considere a história abaixo:

            {history}

            Com base nela, identifique o personagem principal e descreva visualmente sua aparência de forma objetiva, para fins de animação em vídeo.

            Instruções:
            - O resultado deve conter no máximo 100 caracteres.
            - O personagem pode ser uma pessoa, um animal ou um objeto animado, etc.
            - Use linguagem direta e descritiva.
            - Foque apenas no que pode ser representado visualmente
            - Descreva características como: formato do corpo, cor, textura, roupas, acessórios, material, expressão, tamanho, postura, movimentos típicos ou estilo.
            - Não use figuras de linguagem, metáforas ou termos vagos como "bonito", "estranho", "divertido".
            - Não explique o personagem nem narre sua história — apenas descreva visualmente como ele deve parecer.
            - Seja sucinto na resposta, reponda em uma frase, e não use ponto final.
            - Não detalhe muito, apenas o suficiente para "desenhar" o personagem.
            - NÃO especifique descrições não visuais como: "idade", "altura", etc.
            - Use apenas uma única frase longa e contínua.
            - NÃO inclua falas, pensamentos ou emoções.

            Formato da resposta:
            "Aparência do personagem principal descrita de forma objetiva."
            
            Exemplo da resposta:
            Nome do personagem, descrição ...

            Apenas o texto da descrição, sem explicações ou formatações extras.
            """


def formatPromptVideoGeneration(description: str) -> str:
    """
    Otimiza uma descrição narrativa para um prompt direto e objetivo para geração de vídeo.

    Parâmetros:
        description (str): Texto narrativo ou descritivo de uma cena.

    Retorna:
        str: Um prompt formatado com instruções claras para gerar uma descrição visual contínua e precisa.
    """
    prompt_base = f"""
                Você é um modelo de geração de vídeo. Sua tarefa é transformar uma descrição narrativa em uma descrição VISUAL objetiva, com base em elementos concretos e observáveis.

                Instruções conter na resposta:
                - Use apenas uma única frase longa e contínua.
                - O resultado deve conter no máximo 400 caracteres.
                - Utilize linguagem simples.
                - Evite linguagem figurativa, literária ou subjetiva.
                - Descreva apenas o que pode ser visto na cena: roupas, aparência, ações físicas, cores, objetos e cenário.
                - Conecte ações com vírgulas ou palavras simples como "enquanto", "depois", "em seguida".

                Instruções não conter na resposta:
                - NÃO use nomes de pessoas ou locais fictícios.
                - NÃO inclua falas, pensamentos ou emoções.
                - NÃO inclua explicações, interpretações ou contexto narrativo.
                - NÃO use ponto final, ponto-virgula ou aspas.
                - NÃO use nomes de pessoas ou locais fictícios.

                Descrição a ser convertida:
                {description}

                Resposta esperada:
                Uma única frase objetiva e contínua descrevendo a cena de forma visual e direta, sem nomes, falas ou explicações.
                    """
    return prompt_base.strip()


def formatPromptTranslate(conteudo, idioma):
    """
    Gera o prompt para tradução de um conteúdo para o idioma especificado.

    Parâmetros:
        conteudo (str): O texto que deverá ser traduzido.
        idioma (str): O idioma para o qual o conteúdo deverá ser traduzido.

    Retorna:
        str: Um prompt formatado que solicita a tradução do conteúdo, respondida apenas como TEXT.
    """
    return "Traduza para a lingua '"+ idioma+ """

    ' o conteudo:

    "
    """+ conteudo +"""
    "

    Responda apenas no formato texto.

    """

def sendPrompt(prompt):
    """
    Envia o prompt para o serviço de chat utilizando o Client da biblioteca 'ollama' e retorna a resposta.

    Parâmetros:
        prompt (str): O prompt a ser enviado para o modelo de chat.

    Retorna:
        str: A resposta do modelo, com formatações indesejadas (como marcação de JSON) removidas, se necessário.
    """
       
    # print("Prompt:", prompt)
    client = Client(
    host='http://127.0.0.1:11434/',
    headers={'x-some-header': 'some-value'}
    )
    response = client.chat(model='gemma3', messages=[
    {
        'role': 'user',
        'content': prompt,
    },
    ])

    resposta = response.message.content
    print("[Ollama] ✅ Resposta recebida.")
    if "json" in resposta:
        print("[Ollama] 🧹 Limpando marcações de JSON...")
        resposta = resposta.replace("```json", "").replace("```", "")
    return resposta.strip()

def execute(id, temas, licoes):
    
    """
    Função principal que orquestra a criação, tradução e armazenamento de uma história infantil.

    O fluxo de execução é o seguinte:
      1. Seleciona um índice (exemplo: i = 10) e gera a narração da história utilizando 'formatPromptNarracao'.
      2. Processa a resposta JSON para extrair a narração e gera, para cada frase, uma descrição de cena usando 'formatPromptDescriptionScenes'.
      3. Gera o prompt para criação do conteúdo para YouTube com 'formatPromptYoutube' e processa a resposta JSON.
      4. Realiza traduções para múltiplos idiomas (lista de idiomas e siglas definidas) para título, tags, descrição, narração e (para inglês) cenas utilizando 'formatPromptTranslate'.
      5. Armazena o resultado final em um arquivo JSON no caminho especificado.

    Parâmetros:
        ID (str): identificador unico.
        temas (list): Lista de temas para a geração de histórias.
        licoes (list): Lista de lições correspondentes aos temas.

    Retorna:
        (None)
        SAVE PATH_HISTORY:
        "lan" = {
        "title": "....",
        "scenes": ["scenes1","scenes2",...,"scenes N"],
        "narration": ["narration1","narration2",...,"narration N"],
        "tags": ["tag1","tag2",...],
        "description":"..."    

        }
    """

    print("Carregando configs!")

    config = interfaceUtils()
    try:
        resposta = sendPrompt(formatPromptNarracao(temas, licoes))
        print(resposta)
        
        dados_json = json.loads(resposta)
        narracao = dados_json['narration']

    except json.JSONDecodeError as e:
        print(f"Falha ao gerar narração")
        print(f"Erro ao decodificar JSON: {e}")
        print(f"Conteúdo da resposta: {resposta}")

    try:

        narracao_safe = []
        for safenarration in narracao:
            narracao_safe.append(safeTextUnicodeSpeak(safenarration)+ ", ")
        narracao = narracao_safe

    except :
        print(f"Falha ao gerar narração SafeCode")
        print(f"Conteúdo da resposta: {narracao}")

    
   
    dados_json['narration'] = narracao
    scenes = []
    history = "".join(narracao)
    
    try:
            
            resposta_person = sendPrompt(formatPromptDescriptionPerson(history))
            print(resposta_person)
            resposta_person = safeTextUnicodeScene(resposta_person)
    
    except json.JSONDecodeError as e:
            print("Falha ao gerar cena")
            print(f"Erro ao decodificar JSON: {e}")
            print(f"Conteúdo da resposta: {resposta_scene}")

    try:
        for scene in narracao:
            
            resposta_scene_desc = sendPrompt(formatPromptDescriptionScenes(scene, history, resposta_person))
            print(resposta_scene_desc)
            resposta_scene = sendPrompt(formatPromptVideoGeneration(resposta_scene_desc))
            print(resposta_scene_desc)
            scenes.append(safeTextUnicodeScene(resposta_scene))
    
    except json.JSONDecodeError as e:
            print("Falha ao gerar cena")
            print(f"Erro ao decodificar JSON: {e}")
            print(f"Conteúdo da resposta: {resposta_scene}")

    try:
        resposta_youtube = sendPrompt(formatPromptYoutube(history, temas, licoes))
        print(resposta_youtube)
        dados_json_final = json.loads(resposta_youtube)
    except json.JSONDecodeError as e:
        print("Falha ao gerar Descrição Youtube")
        print(f"Erro ao decodificar JSON: {e}")
        print(f"Conteúdo da resposta: {resposta_youtube}")

    try:       

        dados_json_final["title"] = safeTextUnicodeYoutube(dados_json_final["title"]) 
        dados_json_final["tags"] = safeTextUnicodeYoutube(dados_json_final["tags"]) 
        dados_json_final["description"] = safeTextUnicodeYoutube(dados_json_final["description"]) 
        dados_json_final["narration"]=narracao
        dados_json_final["scenes"]=scenes
        
    except :
        print(f"Erro ao gerar connteudo safe")
        
    

    languages = ["árabe","inglês", "espanhol", "francês", "alemão", "italiano", "polonês", "turco", "russo", "holandês", "tcheco", "chinês", "japonês", "húngaro", "coreano", "hindi"]
    siglas = ["ar", "en", "es", "fr", "de", "it", "pl", "tr", "ru", "nl", "cs",  "zh-cn", "ja", "hu", "ko", "hi"]
    dados_multlanguage = {}
    dados_multlanguage["pt"] = dados_json_final
    for j in tqdm(range(len(languages))):
        temp = {}
        resposta_lang = sendPrompt(formatPromptTranslate(dados_json_final["title"], languages[j]))
        print(resposta_lang)
        temp['title'] = safeTextUnicodeYoutube(resposta_lang)
        resposta_lang = sendPrompt(formatPromptTranslate(dados_json_final["tags"], languages[j]))
        print(resposta_lang)
        temp['tags'] = safeTextUnicodeYoutube(resposta_lang)
        resposta_lang = sendPrompt(formatPromptTranslate(dados_json_final["description"], languages[j]))
        print(resposta_lang)
        temp['description'] = safeTextUnicodeYoutube(resposta_lang)
        aux = []
        for n in dados_json_final["narration"]:
            resposta_lang = sendPrompt(formatPromptTranslate(n, languages[j]))
            print(resposta_lang)
            aux.append(safeTextUnicodeSpeak(resposta_lang)+ ", ")
        temp['narration'] = aux
        aux = []
        if siglas[j] == "en":
            for n in dados_json_final["scenes"]:
                resposta_lang = sendPrompt(formatPromptTranslate(n, languages[j]))
                print(resposta_lang)
                aux.append(safeTextUnicodeScene(resposta_lang))
            temp['scenes'] = aux
        dados_multlanguage[siglas[j]] = temp     
            
    
    with open(config["path_history"]+str(id)+"_history.json", 'w', encoding='utf-8') as f:
                json.dump(dados_multlanguage, f, ensure_ascii=False, indent=4)

    


def create_storys(id, temas, licoes):

    """
    Função principal que orquestra a criação, tradução e armazenamento de uma história infantil.

    O fluxo de execução é o seguinte:
      1. Seleciona um índice (exemplo: i = 10) e gera a narração da história utilizando 'formatPromptNarracao'.
      2. Processa a resposta JSON para extrair a narração e gera, para cada frase, uma descrição de cena usando 'formatPromptDescriptionScenes'.
      3. Gera o prompt para criação do conteúdo para YouTube com 'formatPromptYoutube' e processa a resposta JSON.
      4. Realiza traduções para múltiplos idiomas (lista de idiomas e siglas definidas) para título, tags, descrição, narração e (para inglês) cenas utilizando 'formatPromptTranslate'.
      5. Armazena o resultado final em um arquivo JSON no caminho especificado.

    Parâmetros:
        ID (str): identificador unico.
        temas (list): Lista de temas para a geração de histórias.
        licoes (list): Lista de lições correspondentes aos temas.

    Retorna:
        (None)
        SAVE PATH_HISTORY:
        "lan" = {
        "title": "....",
        "scenes": ["scenes1","scenes2",...,"scenes N"],
        "narration": ["narration1","narration2",...,"narration N"],
        "tags": ["tag1","tag2",...],
        "description":"..."    

        }
    """

    print("Carregando configs!")
    
    if platform.system() == "Linux":
        stop_ollama_server()
        start_ollama_server()
        
    execute(id, temas, licoes) 
        
    if platform.system() == "Linux":
        stop_ollama_server()
        
        

def restart():
    import subprocess
    import torch
    import shutil
    import time

    # Para parar o serviço do Ollama
    subprocess.run("taskkill /F /IM ollama.exe", shell=True)
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    # Caminho do cache do Ollama (altere se necessário)
    ollama_cache_path = "C:\\Users\\SeuUsuario\\.ollama"

    # Exclui a pasta do cache (CUIDADO: Isso remove todos os modelos baixados!)
    shutil.rmtree(ollama_cache_path, ignore_errors=True)
    subprocess.run("start ollama", shell=True)
    time.sleep(5)


if __name__ == "__main__":




    print("Iniciando History .....")
    create_storys("testewin9", "joão e o pé de feijão", "honestidade é bom")
