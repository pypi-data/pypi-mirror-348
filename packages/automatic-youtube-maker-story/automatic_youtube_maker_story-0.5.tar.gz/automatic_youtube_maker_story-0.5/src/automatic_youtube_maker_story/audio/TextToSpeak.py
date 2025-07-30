import torch
print(torch.cuda.is_available())  # Deve retornar True
print(torch.version.cuda)         # Mostra a versão CUDA usada
print(torch.cuda.device_count())  # Quantas GPUs detectadas
print(torch.cuda.current_device()) # Indice da GPU atual
print(torch.cuda.get_device_name(0)) # Nome da GPU
import json
import os
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig 
from TTS.tts.models.xtts import Xtts 
import random
from tqdm import tqdm
import argparse
import platform

def interfaceUtils():

    # Chamada config troca para teste direto

    # import utils
    # return utils.config_paths()

    if platform.system() == "Windows":

        return {
            "path_root": "C:\\Users\\will_\\OneDrive\\Documentos\\GitHub\\Contos-Magicos\\",
        "path_base_comfy": "W:\\Youtube\\confyui\\models\\",
        "historic_history": "w:\\Youtube\\ContosMagicos\\controle.json",
        "path_video_out": "W:\\Youtube\\confyui\\comfyui_out\\",
        "path_video": "W:\\Youtube\\confyui\\comfyui_out\\",
        "path_history": "W:\\Youtube\\ContosMagicos\\History\\",
        "path_quiz": "W:\Youtube\\QuizMania\\Quizzes",
        "path_audio" : "W:\\Youtube\\ContosMagicos\\Narration\\audios\\",
        "path_audio_quiz" : "W:\Youtube\\QuizMania\\Narracao",
        "path_FX" : "W:\\Youtube\\FX\\",
        "path_model": "W:\\Youtube\\ContosMagicos\\Narration\\model\\",
        "path_ref": "W:\\Youtube\\ContosMagicos\\Narration\\vozes\\",
        "path_youtube_video": "W:\\Youtube\\ContosMagicos\\youtube_video\\",
        "CLIENT_SECRETS_FILE" : "W:\\Youtube\\ContosMagicos\\client_secrets.json"
        }
    
    if platform.system() == "Linux":

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



def init():
    print("Carregando configs!")

    config = interfaceUtils()


    print("Inicializando TTS")
    # Get device
    print(torch.cuda.is_available())
    device = "cuda" if torch.cuda.is_available() else "cpu"

    

    config_xtts = XttsConfig()
    config_xtts.max_ref_len = 20
    config_xtts.load_json(config["path_model"]+"config.json")
    model = Xtts.init_from_config(config_xtts)
    model.load_checkpoint(config_xtts, checkpoint_dir=config["path_model"], use_deepspeed=True)
    model.cuda()

    print("TTS inicializado")


    # Versão antiga ##################
    # List available 🐸TTS models
    # print(TTS().list_models())

    # Init TTS
    # tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    # tts = TTS(model_path=config["path_model"], config_path=config["path_model"]+"config.json").to(device)
    return model, config



def setTTS(scene, num, id, idioma, tts, config, voice):
    print("Iniciando Narração setTTS .....") 
    print("Computing speaker latents...")
    gpt_cond_latent, speaker_embedding = tts.get_conditioning_latents(audio_path=[config["path_ref"]+voice])
    print("Inference...")

    correcao_ling = {
        "ar":1.5, "cs":1.5, "de":1.5, "en":1.5, "es":1.5,
        "fr":1.5, "it":1.5, "pl":1.5, "nl":1.5, "pt":1,
        "ru":1.5, "tr":1.5, "zh-cn":1.5
    }

    out = tts.inference(
        scene,
        idioma,
        gpt_cond_latent,
        speaker_embedding,
        speed=correcao_ling[idioma]
    )

    # Define o caminho da pasta onde o áudio será salvo
    pasta_destino = os.path.join(config["path_audio"], str(id))

    # Cria a pasta se não existir
    os.makedirs(pasta_destino, exist_ok=True)

    # Define o caminho completo do arquivo
    caminho_arquivo = os.path.join(pasta_destino, f"{id}_Scene_{num}_{idioma}_.wav")

    # Salva o áudio
    torchaudio.save(caminho_arquivo, torch.tensor(out["wav"]).unsqueeze(0), 24000)

    print(f"Áudio salvo em: {caminho_arquivo}")



        

def create_narration(id):

   
    tts, config = init()
    with open(config['path_history']+str(id)+"_history.json", "r", encoding="utf-8") as file:
        history = json.load(file)
    salve_dir = os.path.join(config["path_audio"], str(id))
    voices = [arq for arq in os.listdir(config["path_ref"]) if os.path.isfile(os.path.join(config["path_ref"], arq))]

    for lan in tqdm(history):
        if lan not in ["ja","hu", "ko", "hi"]:
            print("Iniciando Laguage: ", lan)
            voice = random.choice(voices)
            history[lan]["idvoz"] = voice
            scenes = history[lan]['narration']
            with open(config['path_history']+str(id)+"_history.json", "w", encoding="utf-8") as json_file:
                json.dump(history, json_file, indent=4, ensure_ascii=False)
            
            num = 0
            for i in scenes:
                num = num + 1
                
                setTTS(i, num, id, lan, tts, config, voice)
                

        

# def setTTSQUIZ(questions, id, n_quiz, idioma, tts, config, voice):
#     print("Iniciando Narração setTTS .....") 
#     print("Computing speaker latents...")
#     gpt_cond_latent, speaker_embedding = tts.get_conditioning_latents(audio_path=[config["path_ref"]+voice])
#     print("Inference...")
#     params = voice.replace(".wav", "").split("_")
#     print("Parametros:  ")
#     print(params[0])
#     print(float(int(params[1])/100))
#     print(float(int(params[2])/100))
#     print(int(params[3]))
#     print(float(int(params[4])/100))
#     print(float(int(params[5])))
#     print(float(int(params[6])))

#     correcao_ling = {
#         "ar":1.5,
#         "cs":1.5,
#         "de":1.5,
#         "en":1.5,
#         "es":1.5,
#         "fr":1.5,
#         "it":1.5,
#         "pl":1.5,
#         "nl":1.5,
#         "pt":1,
#         "ru":1.5,
#         "tr":1.5,
#         "zh-cn":1.5
#     }
#     print("Taxa final:",float(int(params[2])/100)*correcao_ling[idioma])
#     out = tts.inference(
#         questions[n_quiz]["Pergunta"],
#         idioma,
#         gpt_cond_latent,
#         speaker_embedding,

#         temperature=float(int(params[1])/100), # Add custom parameters here
#         speed=float(int(params[2])/100)*correcao_ling[idioma],
#         top_k=int(params[3]),
#         top_p=float(int(params[4])/100),
#         length_penalty = float(int(params[5])),
#         repetition_penalty = float(int(params[6]))


#     )
#     torchaudio.save(config["path_audio_quiz"]+str(id)+"/"+str(id)+"_question_"+str(n_quiz)+"_"+idioma+"_"+".wav", torch.tensor(out["wav"]).unsqueeze(0), 24000)
#     pauses_text = [
#     "vamos lá, próxima pergunta",
#     "isso aí, bom, próxima pergunta",
#     "vamos lá, continuando",
#     "parabéns, bora continuar, vamos lá",
#     "ótimo, seguimos para a próxima!",
#     "mandou bem, vamos para a próxima rodada",
#     "incrível, próxima questão vindo aí",
#     "continue assim, segue a próxima pergunta",
#     "excelente, vamos para a próxima etapa",
#     "boa, segue a próxima pergunta",
#     "estamos indo bem, próxima pergunta!",
#     "avante, mais uma pergunta",
#     "vamos nessa, próxima questão",
#     "show de bola, pergunta seguinte",
#     "quase lá, vamos para a próxima pergunta",
#     "mandou bem, segue para a próxima!",
#     "cada vez melhor, próxima pergunta vindo aí",
#     "perfeito, prossiga para a próxima pergunta",
#     "ótimo trabalho, vamos continuar",
#     "próxima pergunta, vamos nessa!"
# ]
#     pause = random.choice(pauses_text)
#     out = tts.inference(
#         pause,
#         idioma,
#         gpt_cond_latent,
#         speaker_embedding,

#         temperature=float(int(params[1])/100), # Add custom parameters here
#         speed=float(int(params[2])/100)*correcao_ling[idioma],
#         top_k=int(params[3]),
#         top_p=float(int(params[4])/100),
#         length_penalty = float(int(params[5])),
#         repetition_penalty = float(int(params[6]))


#     )
#     torchaudio.save(config["path_audio_quiz"]+str(id)+"/"+str(id)+"_pause_"+str(n_quiz)+"_"+idioma+"_"+".wav", torch.tensor(out["wav"]).unsqueeze(0), 24000)

#     conclusion_text = [
#         f"A resposta correta é {questions[n_quiz]["Alternativas"][questions[n_quiz]["Resposta"]]}",
#         f"A alternativa certa: {questions[n_quiz]["Alternativas"][questions[n_quiz]["Resposta"]]}",
#         f"A opção correta é {questions[n_quiz]["Alternativas"][questions[n_quiz]["Resposta"]]}",
#         f"{questions[n_quiz]["Alternativas"][questions[n_quiz]["Resposta"]]} é a resposta correta",
#         f"Aqui está: {questions[n_quiz]["Alternativas"][questions[n_quiz]["Resposta"]]}",
#         f"A resposta: {questions[n_quiz]["Alternativas"][questions[n_quiz]["Resposta"]]}",
#         f"Opção correta: {questions[n_quiz]["Alternativas"][questions[n_quiz]["Resposta"]]}",
#         f"{questions[n_quiz]["Alternativas"][questions[n_quiz]["Resposta"]]} foi a alternativa correta",
#         f"{questions[n_quiz]["Alternativas"][questions[n_quiz]["Resposta"]]} - essa é a opção certa",
#         f"O correto é {questions[n_quiz]["Alternativas"][questions[n_quiz]["Resposta"]]}"
#     ]

#     conclusion = random.choice(conclusion_text)
#     out = tts.inference(
#         conclusion,
#         idioma,
#         gpt_cond_latent,
#         speaker_embedding,

#         temperature=float(int(params[1])/100), # Add custom parameters here
#         speed=float(int(params[2])/100)*correcao_ling[idioma],
#         top_k=int(params[3]),
#         top_p=float(int(params[4])/100),
#         length_penalty = float(int(params[5])),
#         repetition_penalty = float(int(params[6]))


#     )
#     torchaudio.save(config["path_audio_quiz"]+str(id)+"/"+str(id)+"_conclusion_"+str(n_quiz)+"_"+idioma+"_"+".wav", torch.tensor(out["wav"]).unsqueeze(0), 24000)


def create_quiznarration( id):      
    tts, config = init()
    with open(config['path_quiz']+str(id)+".json", "r", encoding="utf-8") as file:
        quiz = json.load(file)
    salve_dir = os.path.join(config["path_audio_quiz"], str(id))
    if not os.path.exists(salve_dir):
        os.makedirs(salve_dir)
        print(f"Pasta do projeto de voz criada: {salve_dir}")
        voices = [arq for arq in os.listdir(config["path_ref"]) if os.path.isfile(os.path.join(config["path_ref"], arq))]

        for lan in tqdm(quiz):
            if lan not in ["ja","hu", "ko", "hi"]:
                print("Iniciando Laguage: ", lan)
                voice = random.choice(voices)
                quiz[lan]["idvoz"] = voice
                questions = quiz[lan]
                for i in questions:                    
                    setTTS(questions, id, i, lan, tts, config, voice)
        
                
            
    else:
        print(f"A pasta já existe: {salve_dir}")
        print("Abort!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        

if __name__ == "__main__":
    print("ola")
    create_narration("criancas_0")
