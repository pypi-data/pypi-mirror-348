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


def setWorkflowSD3(prompt, steps_img, cfg_img, wid_img, hei_img, test_prompt):
    
    name = str(test_prompt)+"_"+str(len)+"_"+str(cfg_img)+"_"+str(steps_img)+"_"+"LTX_Image"
    workflow = {
    
  "98": {
    "inputs": {
      "text": prompt,
        "clip": [
        "104",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "99": {
    "inputs": {
      "text": "low quality, worst quality, deformed, distorted, disfigured, motion blur, motion artifacts, fused fingers, bad anatomy, weird hand, ugly, jerky movements",
      "clip": [
        "104",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "100": {
    "inputs": {
      "width": wid_img,
      "height": hei_img,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Empty Latent Image"
    }
  },
  "101": {
    "inputs": {
      "seed": 995320128996075,
      "steps": steps_img,
      "cfg": cfg_img,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1,
      "model": [
        "104",
        0
      ],
      "positive": [
        "98",
        0
      ],
      "negative": [
        "99",
        0
      ],
      "latent_image": [
        "100",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "102": {
    "inputs": {
      "samples": [
        "101",
        0
      ],
      "vae": [
        "104",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "103": {
    "inputs": {
      "images": [
        "102",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "104": {
    "inputs": {
      "ckpt_name": "v1-5-pruned-emaonly-fp16.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "105": {
    "inputs": {
      "filename_prefix": name,
      "images": [
        "102",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
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

def send(id):
    print("Iniciando submisão do video")

    PATH_PROJET =  interfaceUtils()
    print("Carregando historia: ", PATH_PROJET['path_quiz']+str(id)+".json")
    with open(PATH_PROJET['path_quiz']+str(id)+".json", "r", encoding="utf-8") as file:
        quiz = json.load(file)
    i = "Anime"
    for n_quiz in quiz["pt"]:
            num = 0
            for response in quiz["pt"][n_quiz]["Alternativas"]:
                width_img   = 768     #default 768
                height_img  = 768     #default 768
                cfg_img     = 8       #default 8
                steps_img   = 40      #default 40
                prompt = f"create an {i} style {response} illustration image"
                name= str(id) + "_" + str(n_quiz) + "_" + str(num)
                sendWorkflow(setWorkflowSD3(prompt, steps_img, cfg_img, width_img, height_img, name))
    

def teste(id):
    # send("criancas_0")
    ### prompt tratado desenho animado
    print("Iniciando submisão do video")

    PATH_PROJET =  interfaceUtils()
    print("Carregando historia: ", PATH_PROJET['path_quiz']+str(id)+".json")
    with open(PATH_PROJET['path_quiz']+str(id)+".json", "r", encoding="utf-8") as file:
        quiz = json.load(file)
    
    temas = ["realistic", "anime","cartoon", "icon effect"]
    for i in tqdm(temas):    
        for n_quiz in quiz["pt"]:
            num = 0
            for response in quiz["pt"][n_quiz]["Alternativas"]:
                width_img   = 768     #default 768
                height_img  = 768     #default 768
                cfg_img     = 8       #default 8
                steps_img   = 40      #default 40
                prompt = f"create an {i} style {response} illustration image"
                name= str(id) + "_" + str(n_quiz) + "_" + str(num)
                sendWorkflow(setWorkflowSD3(prompt, steps_img, cfg_img, width_img, height_img, name))


if __name__ == "__main__":
    
    teste()