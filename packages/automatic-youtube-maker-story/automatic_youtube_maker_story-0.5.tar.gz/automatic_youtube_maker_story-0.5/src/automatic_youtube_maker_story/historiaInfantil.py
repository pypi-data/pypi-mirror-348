import json
from datetime import datetime, timedelta, time
import os
import subprocess
import video.TextToVideo16x9 as Video 
import youtube.upload as Youtube 
import Editor.pipeToMaker as Maker 
from install_packeges import configPaths
import time
import history as HistGemma3
import audio as NarraXTTS
import utils
from tqdm import tqdm


def stepComplete(step, id):
    """
    Indica a conclusão de uma etapa específica em um processo.

    Parâmetros:
        step (str): Etapa concluída. Deve ser um dos seguintes valores:
            - "narration_complete"
            - "history_complete"
            - "video_complete"
            - "maker_complete"
            - "youtube_complete"
        id (str): Identificador que segue o padrão "<string>_<int>", onde:
            - A parte antes do underline (_) é uma string descritiva.
            - A parte após o underline (_) é um número inteiro representado como string.

    Retorna:
        None

    Exceções:
        ValueError: Se o parâmetro 'step' não estiver entre os valores permitidos ou se 'id' não seguir o padrão "<string>_<int>".
    """
    PATH_CONFIG = utils.config_paths()

    with open(PATH_CONFIG["historic_history"], 'r', encoding='utf-8') as arquivo:
        data = json.load(arquivo)
    
    temp = []
    temp = data[step]
    temp.append(id)
    data[step] = temp

    try:       
        
    
        with open(PATH_CONFIG["historic_history"], "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        print(f"✅ ✅ ✅ STEP: {step} - ID-VIDEO: {id} Complete! ✅ ✅ ✅ ")

    except:
        print(f"❌ ❌ ❌ STEP: {step} - ID-VIDEO: {id} Fail!  ❌ ❌ ❌ ")


def statusProdution():

    PATH_CONFIG = utils.config_paths()

    checkVideos()

    with open(PATH_CONFIG["historic_history"], 'r', encoding='utf-8') as arquivo:
        data = json.load(arquivo)


    titulo_pendentes = []
    titulo_fila = []
    titulo_completo = []

    id_pendente = []
    id_concluidos = []
    id_fila = []


    total_titulos = 0
    id_gen = []
    id_titulo = []
    print("Todos os Temas - Licoes:-----------------------")
    for i in data['conteudo']:
        total_titulos = total_titulos + len(data['conteudo'][i]["theme"])
        for j in range(len(data['conteudo'][i]["theme"])):
            id_val = str(i)+"_"+str(j)
            id_gen.append(id_val)
            titulos_val = f"ID_VIODE: {id_val}    {data['conteudo'][i]['theme'][j]} - {data['conteudo'][i]['lesson'][j]}"
            id_titulo.append(titulos_val)
            print(titulos_val)
    
    
    
    for index, val in enumerate(id_gen):
        flag_nar = False
        flag_vid = False
        flag_his = False
        flag_you = False
        flag_mak = False

        if val in data['narration_complete']:
            flag_nar = True
        if val in data['history_complete']:
            flag_his = True
        if val in data['video_complete']:
            flag_vid = True
        if val in data['maker_complete']:
            flag_mak = True
        if val in data['youtube_complete']:
            flag_you = True

        if flag_nar and flag_vid and flag_his and flag_you and flag_mak:
            titulo_completo.append(id_titulo[index])
            id_concluidos.append(val)
        if (not flag_nar) and (not flag_vid) and (not flag_his) and (not flag_you) and (not flag_mak):
            titulo_fila.append(id_titulo[index])
            id_fila.append(val)

    print(f"❌Todos os Temas - Licoes PENDETES:-----------------------")
    for index, val in enumerate(id_gen):
        flag_nar = False
        flag_vid = False
        flag_his = False
        flag_you = False
        flag_mak = False

        if val in data['narration_complete']:
            flag_nar = True
        if val in data['history_complete']:
            flag_his = True
        if val in data['video_complete']:
            flag_vid = True
        if val in data['maker_complete']:
            flag_mak = True
        if val in data['youtube_complete']:
            flag_you = True
        if (val not in id_fila) and (val not in id_concluidos):
            titulo_pendentes.append(id_titulo[index])
            id_pendente.append(val)
            print(f"IDVIDEO: {val} - Pendencias: ({'Narração' if flag_nar else '' }), ({'Historia' if flag_his else '' }), ({'Video' if flag_vid else '' }), ({'Maker' if flag_mak else '' }), ({'Youtube' if flag_you else '' })")

        

            



    print(f"❌Todos os Temas - Licoes FILA:-----------------------")
    for i in titulo_fila:
        print(i)

    print(f"✅Todos os Temas - Licoes COMPLETOS:-----------------------")
    for i in titulo_completo:
        print(i)

    return id_pendente, id_fila

def priorityQueur(minutos=10000):

    PATH_CONFIG = utils.config_paths()
    print(PATH_CONFIG)
    checkVideos()

    with open(PATH_CONFIG["historic_history"], 'r', encoding='utf-8') as arquivo:
        data = json.load(arquivo)

    itens_p = {
        "Narracao": 10,
        "Video": 260,
        "Historia": 7,
        "Editor": 6,
        "youtube": 2
    }

    titulo_pendentes, titulo_fila = statusProdution()
    schedulen = {}

    if len(titulo_pendentes) != 0:
        for i in titulo_pendentes:
            if i not in  data['history_complete']:
                schedulen[i+"_H"] = {"type":"H","time": itens_p['Historia']}
            if i not in data['narration_complete']:
                schedulen[i+"_N"] = {"type":"N","time": itens_p['Narracao']}
            if i not in data['video_complete']:
                schedulen[i+"_V"] = {"type":"V","time": itens_p['Video']}
            if i not in data['maker_complete'] and i in data['video_complete'] and i in data['narration_complete']and i in data['history_complete']:
                schedulen[i+"_E"] = {"type":"E","time": itens_p['Editor']}
            if i in data['maker_complete'] and i not in data['youtube_complete']:
                schedulen[i+"_Y"] = {"type":"Y","time": itens_p['youtube']}

    if len(titulo_fila) != 0:
        for i in titulo_fila:
            schedulen[i+"_N"] = {"type":"N","time": itens_p['Narracao']}
            schedulen[i+"_H"] = {"type":"H","time": itens_p['Historia']}
            schedulen[i+"_V"] = {"type":"V","time": itens_p['Video']}

    


    
    # # Ordenando pelo campo "time"
    schedulen = sorted(schedulen.items(), key=lambda item: item[1]["time"])
    

    schedulen = dict(schedulen)


    start_process = []
    time_proc = minutos - 30
    for i, v in schedulen.items():
        start_process.append(i)
        time_proc = time_proc - v["time"]
        if time_proc <= 0:
            break

    print("Taks selecionadas: ",start_process)
    

    return start_process


# Verifica se passaram 24 horas
def has_24_hours_passed(last_run):
    last_run = datetime.fromisoformat(last_run)
    return datetime.now() - last_run >= timedelta(hours=24)


def getThemeLesson(id):
    PATH_CONFIG = utils.config_paths()
    print(PATH_CONFIG)
    checkVideos()

    with open(PATH_CONFIG["historic_history"], 'r', encoding='utf-8') as arquivo:
        data = json.load(arquivo)

    hist = id.split("_")

    return data['conteudo'][hist[0]]["theme"][int(hist[1])], data['conteudo'][hist[0]]["lesson"][int(hist[1])]







def checkVideos():
    PATH_CONFIG = utils.config_paths()

    with open(PATH_CONFIG["historic_history"], 'r', encoding='utf-8') as arquivo:
        data = json.load(arquivo)

    lista_videos = {}
    lista_count  = {}
    ult_id = None
    for i in sorted(os.listdir(PATH_CONFIG["path_video_out"])):
        split = i.split("_")
        if len(split) > 1 and split[0] in data['conteudo']:
            id = split[0] +"_"+split[1]
            with open(PATH_CONFIG["path_history"]+str(id)+'_history.json', 'r', encoding='utf-8') as arquivo:
                hist = json.load(arquivo)

            if split[0] in data['conteudo'] and ult_id != id:
                lista_videos[id]= len(hist['en']['scenes'])
                ult_id = id
                count = 0


            if split[0] in data['conteudo'] and ult_id == id:
                count = count + 1
                lista_count[id] = count


    for i in lista_videos:
        if lista_videos[i] == lista_count[i]:
            if i not in  data['video_complete']:
                aux = data['video_complete']
                aux.append(i)
                data['video_complete'] = aux
                with open(PATH_CONFIG["historic_history"], "w", encoding="utf-8") as json_file:
                    json.dump(data, json_file, indent=4, ensure_ascii=False)


    print(f"✅ Lista de Video atualizado")


def runNarration( id):
    
    try:
        
        NarraXTTS.create_narration(id)

        

        print(f"✅ Narração da história: {id} - Concluída!")
        return True

    except subprocess.CalledProcessError as e:
        print("Erro na execução do script:")
        print(e.stderr if e.stderr else "Nenhuma saída de erro capturada.")
        print(f"❌ Narração da história: {id} - Falha!")
        return False




def runHistory(path, id, theme, lesson, config=False):
    
    
    try:
        HistGemma3.create_storys(id, theme, lesson)
        
        print(f"✅ Criação da história: {id} - Concluída!")
        return True
        
    except:
        print(f"❌ Criação da história: {id} - Falha!")
        return False

        


def runVideo(id):
    
    try:
        Video.send(id)
        print(f"✅ Submit Video: {id} - Concluida!")
        return True
    except:
        print(f"❌ Submit Video: {id} - Falhou!")
        return False
    
def runMaker(id):
    
    try:
        Maker.run(id)
        print(f"✅ Submit Maker: {id} - Concluida!")
        return True
    except:
        print(f"❌ Submit Maker: {id} - Falhou!")
        return False
        
def runYoutube(id):
    
    try:
        Youtube.send(id)
        print(f"✅ Submit Maker: {id} - Concluida!")
        return True
    except:
        print(f"❌ Submit Maker: {id} - Falhou!")
        return False


def execute(minutos=10000, config_paths=False):
    if config_paths:
        configPaths()

    PATH_CONFIG = utils.config_paths()
    with open(PATH_CONFIG["historic_history"], 'r', encoding='utf-8') as arquivo:
        data = json.load(arquivo)

    
    tasks = priorityQueur(minutos)

    flag_config_h = config_paths# trocar depois
    flag_config_n = config_paths

    try:
        time_pipe_i = time.time()
        time_task_i = time.time()
        time_task_f = time.time()
        for task in tqdm(tasks):
            task = task.split("_") 
            print(task)
            id = task[0]+"_"+task[1]
            type = task[-1]
            print(f"::::::::::::::::::::::::Submit task: {type} - ID: {id}:::::::::::::::::::::::")
            if type == "H":
                theme , lesson = getThemeLesson(id)
                time_task_i = time.time()
                if runHistory  ( PATH_CONFIG["path_root"], id, theme, lesson, flag_config_h):
                    stepComplete("history_complete", id)
                time_task_f = time.time()
                flag_config_h = False
            if type == "N":
                time_task_i = time.time()
                if runNarration(id):
                    stepComplete("narration_complete", id)
                time_task_f = time.time()
                flag_config_n = False
            if type == "V":
                theme =  None
                lesson = None
                time_task_i = time.time()
                runVideo(                               id)

                time_task_f = time.time()
                flag_config_h = False
            if type == "E":
                time_task_i = time.time()
                if runMaker(                               id):
                    stepComplete("maker_complete", id)

                time_task_f = time.time()
                flag_config_h = False

            # if type == "Y" and has_24_hours_passed(data['API_YOUTUBE']):
            #     time_task_i = time.time()
            #     runYoutube(id)

            #     time_task_f = time.time()
            #     flag_config_h = False
            # elif type == "Y":
            #     print(f"✅ Sem Cotas, próxima tarefa!")
                
            print(f":::::::::::::::::::::::Taks: {type} - Time:{time_task_f - time_task_i} seg:::::::::::::::::::::::")
        time_pipe_f = time.time()
        print(f"✅ ✅ ✅ Pipeline - Time: {time_pipe_f - time_pipe_i} seg - Concluida!✅ ✅ ✅")
        
    except:
        print(f"❌ ❌ ❌ Pipeline travou no Video: {id}! ❌ ❌ ❌")
        raise
    

# improve this list of scenes by optimizing for video generation prompt in the ltx-video model, each scene is a part of the sequence, maintain the consistency of the whole, add video quality specification tags, and consider that each prompt will be submitted separately, in the response keep the same python list pattern:
    
            

            
if __name__ == "__main__":
    execute()
    


