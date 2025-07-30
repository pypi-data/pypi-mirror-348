import torch
import torch.serialization
import json
import os
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
import random
from tqdm import tqdm
import argparse

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

def setTTSQUIZ(text, id, n_quiz, idioma, tts, config, voice):
    print("Iniciando Narração setTTS .....") 
    print("Computing speaker latents...")
    gpt_cond_latent, speaker_embedding = tts.get_conditioning_latents(audio_path=[config["path_ref"]+voice])
    print("Inference...")
    params = voice.replace(".wav", "").split("_")
    print("Parametros:  ")
    print(params[0])
    print(float(int(params[1])/100))
    print(float(int(params[2])/100))
    print(int(params[3]))
    print(float(int(params[4])/100))
    print(float(int(params[5])))
    print(float(int(params[6])))

    correcao_ling = {
        "ar":1.5,
        "cs":1.5,
        "de":1.5,
        "en":1.5,
        "es":1.5,
        "fr":1.5,
        "it":1.5,
        "pl":1.5,
        "nl":1.5,
        "pt":1,
        "ru":1.5,
        "tr":1.5,
        "zh-cn":1.5
    }
    print("Taxa final:",float(int(params[2])/100)*correcao_ling[idioma])
    out = tts.inference(
        text,
        idioma,
        gpt_cond_latent,
        speaker_embedding,

        temperature=float(int(params[1])/100), # Add custom parameters here
        speed=float(int(params[2])/100)*correcao_ling[idioma],
        top_k=int(params[3]),
        top_p=float(int(params[4])/100),
        length_penalty = float(int(params[5])),
        repetition_penalty = float(int(params[6]))


    )
    torchaudio.save(config["path_audio"]+str(id)+"/"+str(id)+"_Scene_"+str(n_quiz)+"_"+idioma+"_"+".wav", torch.tensor(out["wav"]).unsqueeze(0), 24000)


def create_quiznarration(text, id, n_quiz):      
    tts, config = init()
    with open(config['path_history']+str(id)+"_history.json", "r", encoding="utf-8") as file:
        history = json.load(file)
    salve_dir = os.path.join(config["path_audio"], str(id))
    if not os.path.exists(salve_dir):
        os.makedirs(salve_dir)
        print(f"Pasta do projeto de voz criada: {salve_dir}")
        voices = [arq for arq in os.listdir(config["path_ref"]) if os.path.isfile(os.path.join(config["path_ref"], arq))]
        voice = voices[0]
        setTTSQUIZ(text, id, n_quiz, "pt", tts, config, voice)
                
            
    else:
        print(f"A pasta já existe: {salve_dir}")
        print("Abort!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        

if __name__ == "__main__":
    create_quiznarration("vamos lá, próxima pergunta", "pausa", 1)
    create_quiznarration("isso ai, bom, próxima pergunta", "pausa", 2)
    create_quiznarration("vamos lá, continuando", "pausa", 3)
    create_quiznarration("parabens, bora continuar, vamos lá", "pausa", 4)
