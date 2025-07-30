import json
import requests
from datetime import datetime, timedelta
import numpy as np
import time
from tqdm import tqdm
import os

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


# URL da API do ComfyUI
COMFYUI_API_URL = "http://127.0.0.1:8188"




def setWorkflowMochi(len, wid, hei, fps, crf, cfg, prompt, steps, test_prompt):
    tile_size = 256 #256 fix, 160, 128
    overlap = 96  #96 fix,64
    temporal_size = 64
    temporal_overlap = 8
    
    name = str(steps)+"_"+str(test_prompt)+"_"+str(len)+"_"+str(wid)+"_"+str(hei)+"_"+str(fps)+"_"+str(crf)+"_"+str(cfg)+"_"+"MochiLeve"

    # Definição do workflow (substitua conforme necessário)
    workflow = {
    "1": {
        "inputs": {
        "clip_name": "t5xxl_fp16.safetensors",
        "type": "mochi",
        "device": "default"
        },
        "class_type": "CLIPLoader",
        "_meta": {
        "title": "Load CLIP"
        }
    },
    "2": {
        "inputs": {
        "unet_name": "mochi_preview_bf16.safetensors",
        "weight_dtype": "default"
        },
        "class_type": "UNETLoader",
        "_meta": {
        "title": "Load Diffusion Model"
        }
    },
    "3": {
        "inputs": {
        "text":  "The scene is animated in a children's cartoon style, Disney style, with bright, cheerful colors and proportion ratio 16x9; " + prompt + "The scene is animated in a children's cartoon style, Disney style, with bright, cheerful colors and proportion ratio 16x9; ",
        "clip": [
            "1",
            0
        ]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
        "title": "CLIP Text Encode (Prompt)"
        }
    },
    "4": {
        "inputs": {
        "text": "",
        "clip": [
            "1",
            0
        ]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
        "title": "CLIP Text Encode (Prompt)"
        }
    },
    "5": {
        "inputs": {
        "seed": 898052028774897,
        "steps": steps,
        "cfg": cfg,
        "noise":"CPU",
        "sampler_name": "euler",
        "scheduler": "simple",
        "denoise": 1,
        "model": [
            "2",
            0
        ],
        "positive": [
            "3",
            0
        ],
        "negative": [
            "4",
            0
        ],
        "latent_image": [
            "7",
            0
        ]
        },
        "class_type": "KSampler",
        "_meta": {
        "title": "KSampler"
        }
    },
    "6": {
        "inputs": {
        "vae_name": "mochi_vae.safetensors"
        },
        "class_type": "VAELoader",
        "_meta": {
        "title": "Load VAE"
        }
    },
    "7": {
        "inputs": {
        "width": wid,
        "height": hei,
        "length": len,
        "batch_size": 1
        },
        "class_type": "EmptyCosmosLatentVideo",
        "_meta": {
        "title": "EmptyCosmosLatentVideo"
        }
    },
    "8": {
        "inputs": {
           ###### TILED
        "tile_size": tile_size,
        "overlap": overlap,
        "temporal_size": temporal_size,
        "temporal_overlap": temporal_overlap,   
            ########
        "samples": [
            "5",
            0
        ],
        "vae": [
            "6",
            0
        ]
        },
        ###### TILED
        "class_type": "VAEDecodeTiled",
        ###### clasico 
        # "class_type": "VAEDecode",
        "_meta": {
        "title": "VAE Decode"
        }

       
    },
    "9": {
        "inputs": {
        "filename_prefix": name,
        "codec": "vp9",
        "fps": fps,
        "crf": crf,
        "images": [
            "8",
            0
        ]
        },
        "class_type": "SaveWEBM",
        "_meta": {
        "title": "SaveWEBM"
        }
    }
  
    }

    return workflow




def sendWorkflow(prompt):
    payload = {"prompt": prompt}

    try:
        # Envia o prompt
        response = requests.post(f"{COMFYUI_API_URL}/prompt", json=payload)

        if response.status_code == 200:
            data = response.json()
            prompt_id = data.get("prompt_id")
            print(f"Prompt enviado com sucesso! prompt_id: {prompt_id}")
            time_ini_job = datetime.now()

            # Verifica se recebeu um prompt_id
            if not prompt_id:
                print("Não foi possível obter o prompt_id.")
                return
            
            

            while True:
                queue_response = requests.get(f"{COMFYUI_API_URL}/queue")
                if queue_response.status_code == 200:
                    queue_data = queue_response.json()
                    current_jobs = queue_data.get("queue_running", [])
                    pendent_jobs = queue_data.get("queue_pending", [])
                    if  len(pendent_jobs) > 1:
                        print( "Aguardando conclusão...........................................")
                        time_ult_m = (datetime.now() - time_ini_job).total_seconds() / 60
                        print(f"Ultimo job mandado prompt_id: {prompt_id} - {time_ult_m} min")
                        print(f"Fila Ocupada com: {len(current_jobs) + len(pendent_jobs)} jobs!")
                        timeNow(len(current_jobs) + len(pendent_jobs))
                        print("")
                        
                    else:
                        print(f"Fila livre com: {len(current_jobs) + len(pendent_jobs)} jobs!")
                        print("")
                        break
                        
                else:
                    print("Erro ao consultar a fila:", queue_response.status_code)
                time.sleep(60)  # aguarda 2 segundos antes de consultar novamente

        else:
            print(f"Erro ao enviar prompt: {response.status_code}")
            print(response.text)
    except Exception as e:
        print("Erro ao enviar requisição!")
        print(str(e))

def checkVideo(name):
  PATH_VIDEO = interfaceUtils()

  videos = os.listdir(PATH_VIDEO["path_video_out"])
  flag = False
  for file in videos:
    if name  in file:
      flag = True

  if not flag:
    print(f"{name} ----------------------")
    return True
  else:

    print(f"{name} já existe")
    return False

def testeMochi(prompt, cname):
    
    

    heights = [ 384 , 480]
    widths = [ 688 , 848]
    count = -1
    for width in widths:
        count = count + 1
        height = heights[count]
        for liberdade in [
                        7.5,
                        5.5
                        # 5,
                        # 6
                        ]:
            for steps in [
                            20, #fix 20
                            23,
                            25, 
                            # 30
                            ]:
                for len in [
                            157,
                            169
                            ]:    #default 145 (6n+1)

                    
                    #teste MOCHI
                    fps = 24        #default 30 (6n+1)
                    crf = 32        #default 32
                    
                    name = str(steps)+"_"+str(cname)+"_"+str(len)+"_"+str(width)+"_"+str(height)+"_"+str(fps)+"_"+str(crf)+"_"+str(liberdade)+"_"+"MochiLeve"
                    if checkVideo(name): 
                        sendWorkflow(setWorkflowMochi(len, width, height, fps, crf,  liberdade ,prompt, steps, cname))

# tile_size = 128 ou 256 #256, 160, 128
# overlap = 96  #96,64      
# temporal_size = 64
# temporal_overlap = 8
# [07:26<00:00, 22.34s/it]
# [25:51<00:00, 77.59s/it]
# [30:57<00:00, 92.88s/it]
# [33:35<00:00, 100.76s/it]
# [11:48<27:37, 118.37s/it]



     

   




def timeNow(nScenes=1):
    # Data e hora atual
    agora = datetime.now()
    print("Inicio da geração do vídeo#####################")
    print("Data e hora atual:", agora)    
    mtime=2 #média de tempo para gerar 
    termino = agora + nScenes*timedelta(minutes=mtime)
    print(f"Estimativa  ({mtime*nScenes} minutos): {termino} ")
    print("###############################################")

    
def send(id):
    print("Iniciando submisão do video")
    PATH_PROJET =  interfaceUtils()
    print("Carregando historia: ", PATH_PROJET['path_history']+str(id)+"_history.json")
    with open(PATH_PROJET['path_history']+str(id)+"_history.json", "r", encoding="utf-8") as file:
        history = json.load(file)
    num = 0
    for prompt in history["en"]["scenes"]:
      num = num + 1

      width = 848
      height = 480
      len = 145       #default 163
      fps = 24        #default 30
      crf = 32        #default 32
      liberdade = 5.5 #0
      steps = 20 #40
      tile_size = 160 #256, 160, 128
      overlap = 96  #96,64
      temporal_size = 64
      temporal_overlap = 8
      name = str(id)+"_"+str(num)+"_"
      if checkVideo(name):
        sendWorkflow(setWorkflowMochi(len, width, height, fps, crf,  liberdade ,prompt, id, num, steps, "", tile_size, overlap, temporal_size, temporal_overlap))
    
    
    timeNow()

def teste(prompt, cname):

    testeMochi(prompt, cname)

if __name__ == "__main__":
    # send("criancas_0")
    ### prompt tratado desenho animado
#     prompt =  ["A litle girl, radiant in her vibrant red polkadot dress, was running happily through a lush, sunny garden. Colorful flowers of various species  white marguerites, red roses, and yellow sunflowers  blossomed around, creating a mosaic of colors. The soft, green grass stretched as far as the eye could see, and the sun shone intensely, painting everything with a golden glow. Bees buzzed around the flowers, while colorful butterflies fluttered from flower to flower. Julia, with her brown hair and bright eyes, showed a contagious joy while playing, accompanied by the black kitten Ana, observing everything with her bright green eyes; The scene is animated in a children's cartoon style, with bright, cheerful colors.",
#                 "A litle girl, radiant in her vibrant red polkadot dress, was running happily through a lush, sunny garden. Colorful flowers of various species  white marguerites, red roses, and yellow sunflowers  blossomed around, creating a mosaic of colors. The soft, green grass stretched as far as the eye could see, and the sun shone intensely, painting everything with a golden glow. Bees buzzed around the flowers, while colorful butterflies fluttered from flower to flower. Julia, with her brown hair and bright eyes, showed a contagious joy while playing, accompanied by the black kitten Ana, observing everything with her bright green eyes; The scene is animated in a cartoon anime style, with bright, cheerful colors.",
# "A woman with light skin, wearing a blue jacket and a black hat with a veil, looks down and to her right, then back up as she speaks; she has browm hair styled in an updo, light browm eyebrows, and is wearing a white collared shirt under her jacket; the camera remains stationary on her face as she speaks; the background is out of focus, but shows trees and people in period clothing; the scene is captured in real-life footage.",
# "Uma cidadezinha tranquila com casas aconchegantes e um céu azul. Três crianças — Leo (curioso), Maya (imaginativa) e Zack (energético) — estão deitadas na grama, olhando para as nuvens, conversando animadamente sobre embarcar em uma aventura. como desenhos animados em 3D"]
#     temas = ["tratado", "anime","realista", "mochifoco"]

    prompt =  ["A litle girl, radiant in her vibrant red polkadot dress, was running happily through a lush, sunny garden. Colorful flowers of various species  white marguerites, red roses, and yellow sunflowers  blossomed around, creating a mosaic of colors. The soft, green grass stretched as far as the eye could see, and the sun shone intensely, painting everything with a golden glow. Bees buzzed around the flowers, while colorful butterflies fluttered from flower to flower. Julia, with her brown hair and bright eyes, showed a contagious joy while playing, accompanied by the black kitten Ana, observing everything with her bright green eyes; The scene is animated in a children's cartoon style, with bright, cheerful colors.",
               "Helena the Giraffe, a giraffe with soft beige fur and irregular spots that gave her an air of mystery, wore a small necklace of colorful beads. Her long and elegant neck rose towards the blue sky, while her large, brown eyes shone with curiosity and joy. It was a vision of pure adventure in the heart of the safari."]
    temas = ["tratado", "animal"]


    num = 0
    for i in tqdm(prompt):
       teste(i, temas[num])
       num = num + 1


