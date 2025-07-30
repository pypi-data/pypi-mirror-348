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




def setWorkflowMochi(len, wid, hei, fps, crf, cfg, prompt, steps, test_prompt, tile_size, overlap, temporal_size, temporal_overlap):
    
    name = str(steps)+"_"+str(test_prompt)+"_"+str(len)+"_"+str(wid)+"_"+str(hei)+"_"+str(fps)+"_"+str(crf)+"_"+str(cfg)+"_"+"Mochi"

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
        ###### clasico "class_type": "VAEDecode",
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

def setWorkflowLX(len, wid, hei, fps, crf, cfg, prompt, steps, test_prompt):
    
    name = str(steps)+"_"+str(test_prompt)+"_"+str(len)+"_"+str(wid)+"_"+str(hei)+"_"+str(fps)+"_"+str(crf)+"_"+str(cfg)+"_"+"LX_Text"
    
    workflow = {
  "6": {
    "inputs": {
      "text":  prompt ,
        "clip": [
        "38",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Positive Prompt)"
    }
  },
  "7": {
    "inputs": {
      "text": "low quality, worst quality, deformed, distorted, disfigured, motion blur, motion artifacts, fused fingers, bad anatomy, weird hand, ugly, jerky movements",
      "clip": [
        "38",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Negative Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "72",
        0
      ],
      "vae": [
        "44",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "38": {
    "inputs": {
      "clip_name": "t5xxl_fp16.safetensors",
      "type": "ltxv",
      "device": "default"
    },
    "class_type": "CLIPLoader",
    "_meta": {
      "title": "Load CLIP"
    }
  },
  "44": {
    "inputs": {
      "ckpt_name": "ltx-video-2b-v0.9.5.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "69": {
    "inputs": {
      "frame_rate": fps,
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ]
    },
    "class_type": "LTXVConditioning",
    "_meta": {
      "title": "LTXVConditioning"
    }
  },
  "70": {
    "inputs": {
      "width": wid,
      "height": hei,
      "length": len,
      "batch_size": 1
    },
    "class_type": "EmptyLTXVLatentVideo",
    "_meta": {
      "title": "EmptyLTXVLatentVideo"
    }
  },
  "71": {
    "inputs": {
      "steps": steps,
      "max_shift": 2.05,
      "base_shift": 0.95,
      "stretch": True,
      "terminal": 0.1,
      "latent": [
        "70",
        0
      ]
    },
    "class_type": "LTXVScheduler",
    "_meta": {
      "title": "LTXVScheduler"
    }
  },
  "72": {
    "inputs": {
      "add_noise": True,
      "noise_seed": 261471249254103,
      "cfg":cfg,
      "model": [
        "44",
        0
      ],
      "positive": [
        "69",
        0
      ],
      "negative": [
        "69",
        1
      ],
      "sampler": [
        "73",
        0
      ],
      "sigmas": [
        "71",
        0
      ],
      "latent_image": [
        "70",
        0
      ]
    },
    "class_type": "SamplerCustom",
    "_meta": {
      "title": "SamplerCustom"
    }
  },
  "73": {
    "inputs": {
      "sampler_name": "euler"
    },
    "class_type": "KSamplerSelect",
    "_meta": {
      "title": "KSamplerSelect"
    }
  },
  "78": {
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

def setWorkflowWan3(len, wid, hei, fps, crf, cfg, prompt, steps, model, test_prompt):
    
    name = str(steps)+"_"+str(test_prompt)+"_"+str(len)+"_"+str(wid)+"_"+str(hei)+"_"+str(fps)+"_"+str(crf)+"_"+str(cfg)+"_"+str(model).replace(".","_")+"_"+"Wan3"
    
    workflow = {
  "3": {
    "inputs": {
      "seed": 682045780498416,
      "steps": steps,
      "cfg": cfg,
      "sampler_name": "uni_pc",
      "scheduler": "simple",
      "denoise": 1,
      "model": [
        "48",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "40",
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
      "text":  prompt,      "clip": [
        "38",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Positive Prompt)"
    }
  },
  "7": {
    "inputs": {
      "text": "",
      "clip": [
        "38",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Negative Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "39",
        0
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "37": {
    "inputs": {
      "unet_name": model,
      "weight_dtype": "default"
    },
    "class_type": "UNETLoader",
    "_meta": {
      "title": "Load Diffusion Model"
    }
  },
  "38": {
    "inputs": {
      "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
      "type": "wan",
      "device": "default"
    },
    "class_type": "CLIPLoader",
    "_meta": {
      "title": "Load CLIP"
    }
  },
  "39": {
    "inputs": {
      "vae_name": "wan_2.1_vae.safetensors"
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "Load VAE"
    }
  },
  "40": {
    "inputs": {
      "width": wid,
      "height": hei,
      "length": len,
      "batch_size": 1
    },
    "class_type": "EmptyHunyuanLatentVideo",
    "_meta": {
      "title": "EmptyHunyuanLatentVideo"
    }
  },
  "48": {
    "inputs": {
      "shift": 8,
      "model": [
        "37",
        0
      ]
    },
    "class_type": "ModelSamplingSD3",
    "_meta": {
      "title": "ModelSamplingSD3"
    }
  },
  "49": {
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

def setWorkflowWan14(len, wid, hei, fps, crf, cfg, prompt, steps, model, test_prompt):
    
    name = str(steps)+"_"+str(test_prompt)+"_"+str(len)+"_"+str(wid)+"_"+str(hei)+"_"+str(fps)+"_"+str(crf)+"_"+str(cfg)+"_"+str(model).replace(".","_")+"_"+"Wan14"
    
    workflow = {
  "3": {
    "inputs": {
      "seed": 682045780498416,
      "steps": steps,
      "cfg": cfg,
      "sampler_name": "uni_pc",
      "scheduler": "simple",
      "denoise": 1,
      "model": [
        "48",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "40",
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
      "text": prompt,
      "clip": [
        "38",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Positive Prompt)"
    }
  },
  "7": {
    "inputs": {
      "text": "",
      "clip": [
        "38",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Negative Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "39",
        0
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "37": {
    "inputs": {
      "unet_name": model,
      "weight_dtype": "default"
    },
    "class_type": "UNETLoader",
    "_meta": {
      "title": "Load Diffusion Model"
    }
  },
  "38": {
    "inputs": {
      "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
      "type": "wan",
      "device": "default"
    },
    "class_type": "CLIPLoader",
    "_meta": {
      "title": "Load CLIP"
    }
  },
  "39": {
    "inputs": {
      "vae_name": "wan_2.1_vae.safetensors"
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "Load VAE"
    }
  },
  "40": {
    "inputs": {
      "width": wid,
      "height": hei,
      "length": len,
      "batch_size": 1
    },
    "class_type": "EmptyHunyuanLatentVideo",
    "_meta": {
      "title": "EmptyHunyuanLatentVideo"
    }
  },
  "48": {
    "inputs": {
      "shift": 8,
      "model": [
        "37",
        0
      ]
    },
    "class_type": "ModelSamplingSD3",
    "_meta": {
      "title": "ModelSamplingSD3"
    }
  },
  "49": {
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

def setWorkflowWanIMAGEM(len, wid, hei, fps, crf, cfg, prompt, steps, steps_img, cfg_img, wid_img, hei_img, model, test_prompt):
    
    name = str(steps)+"_"+str(test_prompt)+"_"+str(len)+"_"+str(wid)+"_"+str(hei)+"_"+str(fps)+"_"+str(crf)+"_"+str(cfg)+"_"+str(model).replace(".","_")+"_"+"Wan_Image"

    if test_prompt == "tratado":
        path_image = "W:/Youtube/confyui/comfyui_out/promptTratadoMenina/imagem/imagem_LTX_40_5.png"
    
    if test_prompt =="anime":
        path_image = "W:/Youtube/confyui/comfyui_out/Anime/teste_anime.png"

    if test_prompt =="realista":
        path_image = "W:/Youtube/confyui/comfyui_out/realista/teste.png"

    if test_prompt =="mochifoco":
        path_image = "W:/Youtube/confyui/comfyui_out/MochiExemplo/teste.png"
    
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
  "108": {
    "inputs": {
      "samples": [
        "115",
        0
      ],
      "vae": [
        "109",
        0
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "109": {
    "inputs": {
      "vae_name": "wan_2.1_vae.safetensors"
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "Load VAE"
    }
  },
  "110": {
    "inputs": {
      "filename_prefix": name,
      "fps": 16,
      "lossless": False,
      "quality": 90,
      "method": "default",
      "images": [
        "108",
        0
      ]
    },
    "class_type": "SaveAnimatedWEBP",
    "_meta": {
      "title": "SaveAnimatedWEBP"
    }
  },
  "112": {
    "inputs": {
      "text": "low quality, worst quality, deformed, distorted, disfigured, motion blur, motion artifacts, fused fingers, bad anatomy, weird hand, ugly, jerky movements",
      "clip": [
        "119",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Negative Prompt)"
    }
  },
  "113": {
    "inputs": {
      "width": wid,
      "height": hei,
      "length": len,
      "batch_size": 1,
      "positive": [
        "114",
        0
      ],
      "negative": [
        "112",
        0
      ],
      "vae": [
        "109",
        0
      ],
      "clip_vision_output": [
        "117",
        0
      ],
      "start_image": [
        "200",
        0
      ]
    },
    "class_type": "WanImageToVideo",
    "_meta": {
      "title": "WanImageToVideo"
    }
  },
  "114": {
    "inputs": {
      "text": prompt,
      "clip": [
        "119",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Positive Prompt)"
    }
  },
  "115": {
    "inputs": {
      "seed": 987948718394761,
      "steps": steps,
      "cfg": cfg,
      "sampler_name": "uni_pc",
      "scheduler": "simple",
      "denoise": 1,
      "model": [
        "120",
        0
      ],
      "positive": [
        "113",
        0
      ],
      "negative": [
        "113",
        1
      ],
      "latent_image": [
        "113",
        2
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "116": {
    "inputs": {
      "clip_name": "clip_vision_h.safetensors"
    },
    "class_type": "CLIPVisionLoader",
    "_meta": {
      "title": "Load CLIP Vision"
    }
  },
  "117": {
    "inputs": {
      "crop": "none",
      "clip_vision": [
        "116",
        0
      ],
      "image": [
        "102",
        0
      ]
    },
    "class_type": "CLIPVisionEncode",
    "_meta": {
      "title": "CLIP Vision Encode"
    }
  },
  "119": {
    "inputs": {
      "clip_name": "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
      "type": "wan",
      "device": "default"
    },
    "class_type": "CLIPLoader",
    "_meta": {
      "title": "Load CLIP"
    }
  },
  "120": {
    "inputs": {
      "shift": 8,
      "model": [
        "121",
        0
      ]
    },
    "class_type": "ModelSamplingSD3",
    "_meta": {
      "title": "ModelSamplingSD3"
    }
  },
  "121": {
    "inputs": {
      "unet_name": model,
      "weight_dtype": "default"
    },
    "class_type": "UNETLoader",
    "_meta": {
      "title": "Load Diffusion Model"
    }
  },
  "122": {
    "inputs": {
      "filename_prefix": name,
      "codec": "vp9",
      "fps": fps,
      "crf": crf,
      "images": [
        "108",
        0
      ]
    },
    "class_type": "SaveWEBM",
    "_meta": {
      "title": "SaveWEBM"
    }
  },
  "123": {
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
  
  
  
  ,

    "200": {
    "inputs": {
      "image": path_image
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  }

}
    
    ###### 200 foi inserido manualmente




    return workflow

def setWorkflowLTXIMAGEM(len, wid, hei, fps, crf, cfg, prompt, steps, steps_img, cfg_img, wid_img, hei_img, test_prompt):
    
    name = str(steps)+"_"+str(test_prompt)+"_"+str(len)+"_"+str(wid)+"_"+str(hei)+"_"+str(fps)+"_"+str(crf)+"_"+str(cfg)+"_"+str(cfg_img)+"_"+str(steps_img)+"_"+"LTX_Image"

    if test_prompt == "tratado":
        path_image = "W:/Youtube/confyui/comfyui_out/promptTratadoMenina/imagem/imagem_LTX_40_5.png"
    
    if test_prompt =="anime":
        path_image = "W:/Youtube/confyui/comfyui_out/Anime/teste_anime.png"

    if test_prompt =="realista":
        path_image = "W:/Youtube/confyui/comfyui_out/realista/teste.png"

    if test_prompt =="mochifoco":
        path_image = "W:/Youtube/confyui/comfyui_out/MochiExemplo/teste.png"


    
    workflow = {
  "6": {
    "inputs": {
      "text": prompt,
     "clip": [
        "38",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Positive Prompt)"
    }
  },
  "7": {
    "inputs": {
      "text": "low quality, worst quality, deformed, distorted, disfigured, motion blur, motion artifacts, fused fingers, bad anatomy, weird hand, ugly, jerky movements",
      "clip": [
        "38",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Negative Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "72",
        0
      ],
      "vae": [
        "44",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "38": {
    "inputs": {
      "clip_name": "t5xxl_fp16.safetensors",
      "type": "ltxv",
      "device": "default"
    },
    "class_type": "CLIPLoader",
    "_meta": {
      "title": "Load CLIP"
    }
  },
  "44": {
    "inputs": {
      "ckpt_name": "ltx-video-2b-v0.9.5.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "69": {
    "inputs": {
      "frame_rate": fps,
      "positive": [
        "95",
        0
      ],
      "negative": [
        "95",
        1
      ]
    },
    "class_type": "LTXVConditioning",
    "_meta": {
      "title": "LTXVConditioning"
    }
  },
  "71": {
    "inputs": {
      "steps": steps,
      "max_shift": 2.0500000000000003,
      "base_shift": 0.9500000000000002,
      "stretch": True,
      "terminal": 0.10000000000000002,
      "latent": [
        "95",
        2
      ]
    },
    "class_type": "LTXVScheduler",
    "_meta": {
      "title": "LTXVScheduler"
    }
  },
  "72": {
    "inputs": {
      "add_noise": True,
      "noise_seed": 967934410017036,
      "cfg": cfg,
      "model": [
        "44",
        0
      ],
      "positive": [
        "69",
        0
      ],
      "negative": [
        "69",
        1
      ],
      "sampler": [
        "73",
        0
      ],
      "sigmas": [
        "71",
        0
      ],
      "latent_image": [
        "95",
        2
      ]
    },
    "class_type": "SamplerCustom",
    "_meta": {
      "title": "SamplerCustom"
    }
  },
  "73": {
    "inputs": {
      "sampler_name": "euler"
    },
    "class_type": "KSamplerSelect",
    "_meta": {
      "title": "KSamplerSelect"
    }
  },
  "82": {
    "inputs": {
      "img_compression": 40,
      "image": [
        "102",
        0
      ]
    },
    "class_type": "LTXVPreprocess",
    "_meta": {
      "title": "LTXVPreprocess"
    }
  },
  "95": {
    "inputs": {
      "width": wid,
      "height": hei,
      "length": len,
      "batch_size": 1,
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "vae": [
        "44",
        2
      ],
      "image": [
        "82",
        0
      ]
    },
    "class_type": "LTXVImgToVideo",
    "_meta": {
      "title": "LTXVImgToVideo"
    }
  },
  "96": {
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





  },

    "102": {
    "inputs": {
      "image": path_image
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  }




  
  }
    
    ##### AQUI ESTA O STABLE DEFISION ######
    
#     ,
#   "98": {
#     "inputs": {
#       "text": prompt,
#         "clip": [
#         "104",
#         1
#       ]
#     },
#     "class_type": "CLIPTextEncode",
#     "_meta": {
#       "title": "CLIP Text Encode (Prompt)"
#     }
#   },
#   "99": {
#     "inputs": {
#       "text": "low quality, worst quality, deformed, distorted, disfigured, motion blur, motion artifacts, fused fingers, bad anatomy, weird hand, ugly, jerky movements",
#       "clip": [
#         "104",
#         1
#       ]
#     },
#     "class_type": "CLIPTextEncode",
#     "_meta": {
#       "title": "CLIP Text Encode (Prompt)"
#     }
#   },
#   "100": {
#     "inputs": {
#       "width": wid_img,
#       "height": hei_img,
#       "batch_size": 1
#     },
#     "class_type": "EmptyLatentImage",
#     "_meta": {
#       "title": "Empty Latent Image"
#     }
#   },
#   "101": {
#     "inputs": {
#       "seed": 995320128996075,
#       "steps": steps_img,
#       "cfg": cfg_img,
#       "sampler_name": "euler",
#       "scheduler": "normal",
#       "denoise": 1,
#       "model": [
#         "104",
#         0
#       ],
#       "positive": [
#         "98",
#         0
#       ],
#       "negative": [
#         "99",
#         0
#       ],
#       "latent_image": [
#         "100",
#         0
#       ]
#     },
#     "class_type": "KSampler",
#     "_meta": {
#       "title": "KSampler"
#     }
#   },
#   "102": {
#     "inputs": {
#       "samples": [
#         "101",
#         0
#       ],
#       "vae": [
#         "104",
#         2
#       ]
#     },
#     "class_type": "VAEDecode",
#     "_meta": {
#       "title": "VAE Decode"
#     }
#   },
#   "103": {
#     "inputs": {
#       "images": [
#         "102",
#         0
#       ]
#     },
#     "class_type": "PreviewImage",
#     "_meta": {
#       "title": "Preview Image"
#     }
#   },
#   "104": {
#     "inputs": {
#       "ckpt_name": "v1-5-pruned-emaonly-fp16.safetensors"
#     },
#     "class_type": "CheckpointLoaderSimple",
#     "_meta": {
#       "title": "Load Checkpoint"
#     }
#   },
#   "105": {
#     "inputs": {
#       "filename_prefix": name,
#       "images": [
#         "102",
#         0
#       ]
#     },
#     "class_type": "SaveImage",
#     "_meta": {
#       "title": "Save Image"
#     }
#   }
# }

    return workflow

def setWorkflowFinish(len, wid, hei, fps, crf, cfg, prompt, id, num, steps, test_prompt, tile_size, overlap, temporal_size, temporal_overlap):
    
    # name = str(steps)+"_"+str(test_prompt)+"_"+str(len)+"_"+str(wid)+"_"+str(hei)+"_"+str(fps)+"_"+str(crf)+"_"+str(cfg)+"_"+"LX_Text"
    name = str(id)+"_"+str(num)+"_"

    print(f"Nome do video: {name}")

    prompt = "The scene is animated in a children's cartoon style, Disney style, with bright, cheerful colors and proportion ratio 16x9; " + prompt + "; The scene is animated in a children's cartoon style, Disney style, with bright, cheerful colors and proportion ratio 16x9."
    
    # MOCHI
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
        "text":  prompt,
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
        ###### clasico "class_type": "VAEDecode",
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

def testeLTX(prompt, cname):
    
    # 100_tratado_121_768_512_24_32_3.0_LX_Text_00001_
    # 100_realista_121_768_512_24_32_6.0_LX_Text_00001_.webm
    # 100_realista_121_768_512_24_32_4.0_LX_Text_00001_.webm
    # steps 100
    # liberdade 3 < lib < 7
    # resolução 768_512
    # 100_tratado_121_1280_736_24_32_6.0_8.5_20_LTX_Image_00001_
    # 100_realista_121_1280_736_24_32_4.0_8.5_20_LTX_Image_00001_.webm
    # 100_mochifoco_121_1280_736_24_32_3.0_8.5_20_LTX_Image_00001_.webm
    # resolução 1280_736
    # step 100
    # liberdade 4.0 < lib 


    PATH_VIDEO = interfaceUtils()

    videos = os.listdir(PATH_VIDEO["path_video_out"])
    for liberdade_add in tqdm(np.arange(2, 7, 1)):
      for steps_add in np.arange(25, 101, 25):
            
            #teste LTX Text-to-Video
            width = 704       #default 704
            height = 480      #default 480
            len = (24*5)+1    #default 121
            fps = 24          #default 24
            crf = 32          #default 32
            liberdade = 3     #default 3
            steps = 40        #default 40
            
            name = str(int(steps_add))+"_"+str(cname)+"_"+str(len)+"_"+str(width)+"_"+str(height)+"_"+str(fps)+"_"+str(crf)+"_"+str(float(liberdade_add))+"_"+"LX_Text"
            flag = False
            for file in videos:
              if name in file:
                flag = True

            if not flag:
              sendWorkflow(setWorkflowLX(len, width, height, fps, crf,  float(liberdade_add) ,prompt, int(steps_add), cname))
              print(f"{name} ----------------------")
            else:
              print(f"{name} já existe")
          
            #teste LTX Text-to-Video
            width = 768       #default 704
            height = 512      #default 480
            len = (24*5)+1    #default 121
            fps = 24          #default 24
            crf = 32          #default 32
            name = str(int(steps_add))+"_"+str(cname)+"_"+str(len)+"_"+str(width)+"_"+str(height)+"_"+str(fps)+"_"+str(crf)+"_"+str(float(liberdade_add))+"_"+"LX_Text"
            flag = False

            for file in videos:
              if name in file:
                flag = True

            if not flag:
              sendWorkflow(setWorkflowLX(len, width, height, fps, crf,  float(liberdade_add) ,prompt, int(steps_add), cname))
              print(f"{name} ----------------------")
            else:
              print(f"{name} já existe")
            
            #teste LTX - IMAGE - 1280x720
            width = 704       #default 704
            height = 480      #default 480
            len = (24*5)+1    #default 121
            fps = 24          #default 24
            crf = 32          #default 32
            liberdade = 3     #default 3
            steps = 40        #default 40

            width_img   = 768     #default 768
            height_img  = 768     #default 768
            cfg_img     = 8.5       #default 8
            steps_img   = 20      #default 40
            name = str(int(steps_add))+"_"+str(cname)+"_"+str(len)+"_"+str(width)+"_"+str(height)+"_"+str(fps)+"_"+str(crf)+"_"+str(float(liberdade_add))+"_"+str(float(cfg_img))+"_"+str(int(steps_img))+"_"+"LTX_Image"
            flag = False
            for file in videos:
              if name  in file:
                flag = True

            if not flag:
              sendWorkflow(setWorkflowLTXIMAGEM(len, width, height, fps, crf,  float(liberdade_add) ,prompt, int(steps_add), int(steps_img),float(cfg_img), width_img, height_img, cname))
              print(f"{name} ----------------------")
            else:
              print(f"{name} já existe")

            #teste LTX - IMAGE - 1280x720
            width = 1280       #default 704
            height = 736      #default 480
            len = (24*5)+1    #default 121
            fps = 24          #default 24
            crf = 32          #default 32

            width_img   = 520     #default 768
            height_img  = 520     #default 768
            cfg_img     = 8.5       #default 8
            steps_img   = 20      #default 40
            name = str(int(steps_add))+"_"+str(cname)+"_"+str(len)+"_"+str(width)+"_"+str(height)+"_"+str(fps)+"_"+str(crf)+"_"+str(float(liberdade_add))+"_"+str(float(cfg_img))+"_"+str(int(steps_img))+"_"+"LTX_Image"
            flag = False
            for file in videos:
              if name in file:
                flag = True

            if not flag:
              sendWorkflow(setWorkflowLTXIMAGEM(len, width, height, fps, crf,  float(liberdade_add) ,prompt, int(steps_add), int(steps_img),float(cfg_img), width_img, height_img, cname))
              print(f"{name} ----------------------")
            else:
              print(f"{name} já existe")



def testeWan(prompt, cname):
    
    heights = [720, 480, 384]
    widths = [1280, 832, 664]
    fps = 16        #default 16
    crf = 32        #default 32
    
    cfg_img     = 8       #default 8
    steps_img   = 40      #default 40
    count = -1
    for width in widths:
      count = count + 1
      height = heights[count]
      width_img   = width     #default 768
      height_img  = height     #default 768
      for liberdade in [4.5, 5, 5.5]:
        for steps in [ 10,15,20,25,40]:
            if height < 480:
              
              name = str(steps)+"_"+str(cname)+"_"+str(len)+"_"+str(width)+"_"+str(height)+"_"+str(fps)+"_"+str(crf)+"_"+str(liberdade)+"_"+str("wan2.1_t2v_1.3B_fp16.safetensors").replace(".","_")+"_"+"Wan3"
              if checkVideo(name): 
                sendWorkflow(setWorkflowWan3(len, width, height, fps, crf,  liberdade ,prompt, steps, "wan2.1_t2v_1.3B_fp16.safetensors", cname))
              
              name = str(steps)+"_"+str(cname)+"_"+str(len)+"_"+str(width)+"_"+str(height)+"_"+str(fps)+"_"+str(crf)+"_"+str(liberdade)+"_"+str("wan2.1_t2v_14B_fp16.safetensors").replace(".","_")+"_"+"Wan14"
              if checkVideo(name): 
                sendWorkflow(setWorkflowWan14(len, width, height, fps, crf,  liberdade ,prompt, steps, "wan2.1_t2v_14B_fp16.safetensors", cname))
              
              
              name = str(steps)+"_"+str(cname)+"_"+str(len)+"_"+str(width)+"_"+str(height)+"_"+str(fps)+"_"+str(crf)+"_"+str(liberdade)+"_"+str("wan2.1_i2v_480p_14B_fp16.safetensors").replace(".","_")+"_"+"Wan_Image"
              if checkVideo(name): 
                sendWorkflow(setWorkflowWanIMAGEM(len, width, height, fps, crf,  liberdade ,prompt, steps, steps_img,cfg_img,width_img, height_img, "wan2.1_i2v_480p_14B_fp16.safetensors", cname))


            if height == 720: 
              

              name = str(steps)+"_"+str(cname)+"_"+str(len)+"_"+str(width)+"_"+str(height)+"_"+str(fps)+"_"+str(crf)+"_"+str(liberdade)+"_"+str("wan2.1_t2v_14B_fp16.safetensors").replace(".","_")+"_"+"Wan14"
              if checkVideo(name): 
                sendWorkflow(setWorkflowWan14(len, width, height, fps, crf,  liberdade ,prompt, steps, "wan2.1_t2v_14B_fp16.safetensors", cname))
              
              name = str(steps)+"_"+str(cname)+"_"+str(len)+"_"+str(width)+"_"+str(height)+"_"+str(fps)+"_"+str(crf)+"_"+str(liberdade)+"_"+str("wan2.1_i2v_720p_14B_fp16.safetensors").replace(".","_")+"_"+"Wan_Image"
              if checkVideo(name): 
                sendWorkflow(setWorkflowWanIMAGEM(len, width, height, fps, crf,  liberdade ,prompt, steps, steps_img,cfg_img,width_img, height_img, "wan2.1_i2v_720p_14B_fp16.safetensors", cname))
    

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
    
    heights = [  
              480,
              768, 
              720
              
              ]
    widths = [
              848,
             1280, 
             1280
              
              ]
    count = -1
    for width in widths:
      count = count + 1
      height = heights[count]
      for liberdade in [
                        5.5,
                        # 5,
                        # 6
                        ]:
        for steps in [
                      20, #fix 20
                      # 25, 
                      # 30
                      ]:
          for len in [
                        49,
                        133,
                        145, 
                        157,
                        169
                        ]:    #default 145 (6n+1)

              
              #teste MOCHI
              fps = 8        #default 30 (6n+1)
              crf = 32        #default 32
              tile_size = 160 #256, 160, 128
              overlap = 96  #96,64
              temporal_size = 64
              temporal_overlap = 8
              name = str(steps)+"_"+str(cname)+"_"+str(len)+"_"+str(width)+"_"+str(height)+"_"+str(fps)+"_"+str(crf)+"_"+str(liberdade)+"_"+"Mochi"
              if checkVideo(name): 
                sendWorkflow(setWorkflowMochi(len, width, height, fps, crf,  liberdade ,prompt, steps, cname, tile_size, overlap, temporal_size, temporal_overlap))
     





   




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

      width = 688
      height = 384
      len = 145       #default 163
      fps = 24        #default 30
      crf = 32        #default 32
      liberdade = 6 #0
      steps = 20 #40
      name = str(id)+"_"+str(num)+"_"
      if checkVideo(name):
        sendWorkflow(setWorkflowFinish(len, width, height, fps, crf,  liberdade ,prompt, id, num, steps, ""))
    
    
    timeNow()

def teste(prompt, cname):

    testeMochi(prompt, cname)
    # testeLTX(prompt, cname)
    testeWan(prompt, cname)

if __name__ == "__main__":
    # send("criancas_0")
    ### prompt tratado desenho animado
#     prompt =  ["A litle girl, radiant in her vibrant red polkadot dress, was running happily through a lush, sunny garden. Colorful flowers of various species  white marguerites, red roses, and yellow sunflowers  blossomed around, creating a mosaic of colors. The soft, green grass stretched as far as the eye could see, and the sun shone intensely, painting everything with a golden glow. Bees buzzed around the flowers, while colorful butterflies fluttered from flower to flower. Julia, with her brown hair and bright eyes, showed a contagious joy while playing, accompanied by the black kitten Ana, observing everything with her bright green eyes; The scene is animated in a children's cartoon style, with bright, cheerful colors.",
#                 "A litle girl, radiant in her vibrant red polkadot dress, was running happily through a lush, sunny garden. Colorful flowers of various species  white marguerites, red roses, and yellow sunflowers  blossomed around, creating a mosaic of colors. The soft, green grass stretched as far as the eye could see, and the sun shone intensely, painting everything with a golden glow. Bees buzzed around the flowers, while colorful butterflies fluttered from flower to flower. Julia, with her brown hair and bright eyes, showed a contagious joy while playing, accompanied by the black kitten Ana, observing everything with her bright green eyes; The scene is animated in a cartoon anime style, with bright, cheerful colors.",
# "A woman with light skin, wearing a blue jacket and a black hat with a veil, looks down and to her right, then back up as she speaks; she has browm hair styled in an updo, light browm eyebrows, and is wearing a white collared shirt under her jacket; the camera remains stationary on her face as she speaks; the background is out of focus, but shows trees and people in period clothing; the scene is captured in real-life footage.",
# "Uma cidadezinha tranquila com casas aconchegantes e um céu azul. Três crianças — Leo (curioso), Maya (imaginativa) e Zack (energético) — estão deitadas na grama, olhando para as nuvens, conversando animadamente sobre embarcar em uma aventura. como desenhos animados em 3D"]
#     temas = ["tratado", "anime","realista", "mochifoco"]

    prompt =  ["A litle girl, radiant in her vibrant red polkadot dress, was running happily through a lush, sunny garden. Colorful flowers of various species  white marguerites, red roses, and yellow sunflowers  blossomed around, creating a mosaic of colors. The soft, green grass stretched as far as the eye could see, and the sun shone intensely, painting everything with a golden glow. Bees buzzed around the flowers, while colorful butterflies fluttered from flower to flower. Julia, with her brown hair and bright eyes, showed a contagious joy while playing, accompanied by the black kitten Ana, observing everything with her bright green eyes; The scene is animated in a children's cartoon style, with bright, cheerful colors."]
    temas = ["tratado"]


    num = 0
    for i in tqdm(prompt):
       teste(i, temas[num])
       num = num + 1


