
from moviepy import  VideoFileClip, AudioFileClip, concatenate_videoclips, afx, CompositeAudioClip, vfx, CompositeVideoClip, TextClip

import os
import math
import random
from datetime import timedelta
import json
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




def findVideos(id_selec, config):
    lista_videos = {}
    print("Vídeos Selecionados:------")
    for i in sorted(os.listdir(config["path_video"])):
        split = i.split("_")
        if len(split) > 1:
            id = split[0]+"_"+split[1]

            if str(id_selec) == str(id):
                num = split[2]
                temp_video =VideoFileClip(config["path_video"]+i) 
                lista_videos[str(num)] = temp_video.with_effects([vfx.MultiplySpeed(0.35)])
    lista_videos = dict(sorted(lista_videos.items(), key=lambda x: int(x[0])))
    return lista_videos

            


def findAudios(id_selec, config):
    
    lista_audio = {}
    dir_video = os.path.join(config["path_audio"], str(id_selec))
    pasta = sorted(list(os.listdir(dir_video)))
    print("Audios Selecionados:------")
    for lang in ["pt","ar", "en", "es", "fr", "de", "it", "pl", "tr", "ru", "nl", "cs",  "zh-cn"]:
        aux = {}
        for i in pasta:
            split = i.split("_")
            id = split[0]+"_"+split[1]
            if str(id_selec) == str(id) and split[4] == lang:
                num = split[3].replace(".wav","")
                aux[str(num)]=AudioFileClip(config["path_audio"]+"/"+str(id)+"/"+i)
        lista_audio[lang] = dict(sorted(aux.items(), key=lambda x: int(x[0])))

    return lista_audio
            

def findFX(config):
    print("Buscando FX-------")
    fx_list = os.listdir(config["path_FX"])
    fx_selec = random.randint(0, len(fx_list)-1)
    return config["path_FX"]+fx_list[fx_selec]


# Converte segundos (float ou int) para string no formato SRT
def seg_to_srt_time(seg):
    td = timedelta(seconds=seg)
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((td.total_seconds() - total_seconds) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# Gera arquivo .srt
def gerar_srt(narration, times, output_file="legenda.srt"):
    with open(output_file, "w", encoding="utf-8") as f:
        for i, (texto, (start, end)) in enumerate(zip(narration, times), 1):
            f.write(f"{i}\n")
            f.write(f"{seg_to_srt_time(start)} --> {seg_to_srt_time(end)}\n")
            f.write(f"{texto.strip()}\n\n")
    print(f"Arquivo '{output_file}' gerado com sucesso.")


    



def multiplefaixe(id, path_content):
    import subprocess
    cmd = [
        "ffmpeg",
        "-i", path_content+"/"+str(id)+".mp4",  # entrada de vídeo sem áudio

        # Entradas de áudio (uma para cada idioma)
        "-i", path_content+"/"+str(id)+"_pt.mp3",
        "-i", path_content+"/"+str(id)+"_en.mp3",
        "-i", path_content+"/"+str(id)+"_es.mp3",
        "-i", path_content+"/"+str(id)+"_fr.mp3",
        "-i", path_content+"/"+str(id)+"_de.mp3",
        "-i", path_content+"/"+str(id)+"_it.mp3",
        "-i", path_content+"/"+str(id)+"_pl.mp3",
        "-i", path_content+"/"+str(id)+"_tr.mp3",
        "-i", path_content+"/"+str(id)+"_ru.mp3",
        "-i", path_content+"/"+str(id)+"_nl.mp3",
        "-i", path_content+"/"+str(id)+"_cs.mp3",
        "-i", path_content+"/"+str(id)+"_zh-cn.mp3",
        "-i", path_content+"/"+str(id)+"_ar.mp3",

        # Mapeamento de streams: vídeo + 13 faixas de áudio
        "-map", "0:v",
        "-map", "1:a",  # ar
        "-map", "2:a",  # en
        "-map", "3:a",  # es
        "-map", "4:a",  # fr
        "-map", "5:a",  # de
        "-map", "6:a",  # it
        "-map", "7:a",  # pl
        "-map", "8:a",  # tr
        "-map", "9:a",  # ru
        "-map", "10:a", # nl
        "-map", "11:a", # cs
        "-map", "12:a", # zh-cn
        "-map", "13:a", # pt

        # Cópia do vídeo e codificação do áudio
        "-c:v", "copy",
        "-c:a", "aac",

        # Definição de metadados por faixa de áudio
        "-metadata:s:a:0", "language=por",
        "-metadata:s:a:1", "language=eng",
        "-metadata:s:a:2", "language=spa",
        "-metadata:s:a:3", "language=fra",
        "-metadata:s:a:4", "language=deu",
        "-metadata:s:a:5", "language=ita",
        "-metadata:s:a:6", "language=pol",
        "-metadata:s:a:7", "language=tur",
        "-metadata:s:a:8", "language=rus",
        "-metadata:s:a:9", "language=nld",
        "-metadata:s:a:10", "language=ces",
        "-metadata:s:a:11", "language=zho",
        "-metadata:s:a:12", "language=ara",

        path_content+"/"+str(id)+"_multiaudio.mp4"
    ]

    subprocess.run(cmd)


def run(id):
    print("Iniciando Edição")
    config = interfaceUtils()
    with open(config['path_history']+str(id)+"_history.json", "r", encoding="utf-8") as file:
        history = json.load(file)
    content_dir = os.path.join(config["path_youtube_video"], str(id))
    if not os.path.exists(content_dir):
        os.makedirs(content_dir)

    set_audios = findAudios(id, config)
    set_videos = findVideos(id, config)
    set_fx     = findFX(config)

    

    print("Mixando audio......")

    fx = AudioFileClip(set_fx)
    fx = fx.with_effects([afx.MultiplyVolume(0.2)])

    
    
    for lang in ["ar", "en", "es", "fr", "de", "it", "pl", "tr", "ru", "nl", "cs",  "zh-cn", "pt"]:
        TimeNarration = []
        aux_fx = fx
        print("IDIOMA: ",lang)
        print(len(set_audios[lang])+1)
        for audio in range(1,len(set_audios[lang])+1):


            if audio == 1:

                print("audio num:",audio)
                duration_audio = set_audios[lang][str(audio)].duration
                duration_video = set_videos[str(audio)].duration
                aux_temp = set_audios[lang][str(audio)]
                pausa = (duration_video - min(duration_audio, duration_video)) / 2

                
                aux_temp = aux_temp.subclipped(0, min(duration_audio, duration_video))
                aux_temp = aux_temp.with_start(pausa)
                aux_temp = aux_temp.with_end(pausa+min(duration_audio, duration_video))
                set_audios[lang][str(audio)] = aux_temp

                print("Timeline")
                print(aux_temp.start)
                print(aux_temp.end)
            else:
                print("audio num:",audio)
                duration_audio = set_audios[lang][str(audio)].duration
                duration_video = set_videos[str(audio)].duration
                aux_temp = set_audios[lang][str(audio)]
                pausa = (duration_video - min(duration_audio, duration_video)) / 2

                aux_temp = aux_temp.subclipped(0, min(duration_audio, duration_video))
                
                aux_temp = aux_temp.with_start(end_clip+pausa)
                aux_temp = aux_temp.with_end(end_clip+pausa+min(duration_audio, duration_video))
                set_audios[lang][str(audio)] = aux_temp
                print("Timeline")
                print(aux_temp.start)
                print(aux_temp.end)
            end_clip = pausa + aux_temp.end
            TimeNarration.append((aux_temp.start, aux_temp.end))
        
        
        gerar_srt(history[lang]['narration'], TimeNarration, output_file=content_dir+"/"+str(id)+"_"+lang+".srt")
        lista_audio_final = []
        print(set_audios[lang].keys())
        for i in set_audios[lang]:
            print(i)
            lista_audio_final.append(set_audios[lang][str(i)])
        print(lista_audio_final)
        narracao = CompositeAudioClip(lista_audio_final)
        print(narracao.start)
        print(narracao.end)
        narracao.close()
        

        print("Ajustando Audio FX......")
        aux_fx = aux_fx.with_effects([afx.AudioLoop(duration=narracao.duration)])
        aux_fx.close()

        print("Fechando audio completo......")
        audio_final = CompositeAudioClip([narracao, aux_fx])
        print(audio_final.start)
        print(audio_final.end)
        audio_final.close()

        print("Salvando Audio......")

        audio_final.write_audiofile(content_dir+"/"+str(id)+"_"+lang+".mp3")
        audio_final.close()
        
        

    print("Montando completo......")
    # # Concatenar os vídeos com seus áudios
    lista_videos_final = []
    for i in set_videos:
        lista_videos_final.append(set_videos[i])
    final_video = concatenate_videoclips(lista_videos_final)

    final_video.close()


    # Redimensiona para 1920x1080
    print("Forçando Full HD......")
    
    final_video = final_video.with_effects([vfx.Resize((1920,1080))])
    final_video.write_videofile(content_dir+"/"+str(id)+".mp4")
    print("Renderizando......")
    # 3 Idiomas videos:
    
    for lang in ['pt', 'en', 'zh-cn']:
        temp_final = final_video.with_audio(AudioFileClip(content_dir+"/"+str(id)+"_"+lang+".mp3"))
        # final_video = final_video.with_effects([vfx.MultiplySpeed(0.95)])
        
        temp_final.close()
        
        print("Salvando Mídia......")
        temp_final.write_videofile(content_dir+"/"+str(id)+"_"+lang+".mp4")
        makeShorts(id, content_dir, lang)

    multiplefaixe(id, content_dir)

def makeShorts(id, content_dir, lang, duracao_maxima=57):
    print("Iniciando Edição Shorts")
    
    # Carrega o vídeo
    video = VideoFileClip(content_dir+"/"+str(id)+"_"+lang+".mp4")
    
    
    # Obtém a duração total do vídeo (em segundos)
    duracao_total = video.duration
    
    # Calcula quantos clipes serão gerados
    numero_de_clipes = math.ceil(duracao_total / duracao_maxima)
    
    # Cria pasta para os clipes, se não existir
    pasta_saida = "clipes"
    os.makedirs(pasta_saida, exist_ok=True)

    print(f"Duração do vídeo: {duracao_total:.2f} segundos")
    print(f"Dividindo em {numero_de_clipes} clipes de até {duracao_maxima} segundos...")

    # Gera os clipes
    for i in range(numero_de_clipes):
        inicio = i * duracao_maxima
        fim = min((i + 1) * duracao_maxima, duracao_total)
        clip = video.subclipped(inicio, fim)
        # Resolução original
        largura_original, altura_original = clip.size
        print(f"Resolução original: {largura_original}x{altura_original}")
        
        # Calcula a largura necessária para manter proporção 9:16 com a altura original
        largura_crop = altura_original * 9 / 16

        # Garante que não exceda a largura original
        if largura_crop > largura_original:
            raise ValueError("O vídeo é muito estreito para cropar para 9:16 com a altura original.")

        # Define coordenadas de crop centralizado
        x_centro = largura_original / 2
        x1 = x_centro - largura_crop / 2
        x2 = x_centro + largura_crop / 2

        # Aplica o crop centralizado e redimensiona para 1080x1920
        video_cortado = clip.with_effects([vfx.Crop(x1=x1, x2=x2)])
        video_redimensionado = video_cortado.with_effects([vfx.Resize((1080,1920))])

                # Texto de parte (ex: "Parte 1/3")
        texto_parte = f"Parte {str(i+1)}/{str(numero_de_clipes)}"
        
        if platform.system() == "Windows":
            font_path = "C:/Windows/Fonts/impact.ttf"
        else:
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # exemplo no Linux

        
        
        texto = TextClip(
            text = texto_parte,
            font_size=70,
            color='white',
            font=font_path,
            bg_color='black',
            margin  = (10,5),
            size=(640, 100),  # largura total, altura do fundo
            method='label'  
        ).with_duration(video_redimensionado.duration)

        # Posição: inferior e centralizado
        texto = texto.with_position(lambda t: ('center', 50+t))

        # Composição final
        video_redimensionado = CompositeVideoClip([video_redimensionado, texto])

        # Exporta o vídeo
        video_redimensionado.write_videofile(content_dir+"/"+str(id)+"_"+lang+"_SHORTS_"+str(i)+".mp4")

        # Libera os recursos
        video_redimensionado.close()
        print(f"Vídeo salvo em: {content_dir+'/'+str(id)+'_'+lang+'_SHORTS_'+str(i)+'.mp4'}")








if __name__ == "__main__":

    # print("Iniciando Edição .....")
    # parser = argparse.ArgumentParser(description="Configurações e input do id da historia")
    # parser.add_argument("id", type=str, help="ID da historia a qual será gerada as narrações")
    # parser.add_argument("--config", type=bool, help="Redefinir caminhos do projeto", default=False)

    # args = parser.parse_args()
    # print(f"ID História: {args.id}")
    # print(f"--config: {args.config}")

    # if args.config :
    #     utils.config()
    run("criancas_0")

    # print("Iniciando Edição")
    # config = interfaceUtils()
    # content_dir = os.path.join(config["path_youtube_video"], "criancas_0")
    # if not os.path.exists(content_dir):
    #     os.makedirs(content_dir)
    # makeShorts("criancas_0", content_dir, 'pt')
