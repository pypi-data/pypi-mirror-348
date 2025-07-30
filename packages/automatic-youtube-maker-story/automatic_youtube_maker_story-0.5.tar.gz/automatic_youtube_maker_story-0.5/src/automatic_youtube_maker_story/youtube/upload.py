#!/usr/bin/python

import http.client as httplib
import httplib2
import json
import os
import random
import sys
from datetime import timedelta, time, datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
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


# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
  httplib.IncompleteRead, httplib.ImproperConnectionState,
  httplib.CannotSendRequest, httplib.CannotSendHeader,
  httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.cloud.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets


# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl", "https://www.googleapis.com/auth/youtube"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__)))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


















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
    PATH_CONFIG = interfaceUtils()

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




# Autenticação e criação do serviço
def get_authenticated_service():

  PATH_PROJET =  interfaceUtils()
  flow = flow_from_clientsecrets(PATH_PROJET["CLIENT_SECRETS_FILE"],
    scope=YOUTUBE_UPLOAD_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))




def upload_legend(youtube,content_dir,video_id, id, history, lang_ori):
    youtube = get_authenticated_service()
    languages = ["ar", "en", "es", "fr", "de", "it", "pl", "tr", "ru", "nl", "cs", "zh-cn", "pt"]

    # Upload de legendas e inserção de descrições traduzidas
    for lang in languages:
        srt_file = content_dir+"/"+str(id)+"_"+lang+".srt"
        if os.path.exists(srt_file):
            caption_body = {
                "snippet": {
                    "videoId": video_id,
                    "language": lang,
                    "name": f"Legenda {lang}",
                    "isDraft": False
                }
            }
            caption_media = MediaFileUpload(srt_file, mimetype="application/octet-stream", resumable=True)
            caption_request = youtube.captions().insert(part="snippet", body=caption_body, media_body=caption_media)
            caption_response = caption_request.execute()
            print(f"Legenda {lang} enviada com ID: {caption_response['id']}")
        else:
            print(f"[Aviso] Arquivo de legenda não encontrado: {srt_file}")

    # Inserir descrições em múltiplos idiomas
    for lang in languages:
        if lang == lang_ori:
            continue  # já está na principal
        translation_body = {
            "snippet": {
                "videoId": video_id,
                "language": lang,
                "title": history[lang]['title'],
                "description": history[lang]['description']
            }
        }

        youtube.videos().insert(part="snippet", body=translation_body).execute()
        print(f"Descrição em {lang} atualizada.")



# Função de upload e agendamento
def upload_video(youtube, file_path, title, description, tags, scheduled_time, lang, pattn_short):

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "27",  # Categoria "Education"
        },
        "status": {
            "privacyStatus": "private",  # Começa como privado
            "publishAt": scheduled_time.isoformat("T") + "Z",  # Formato RFC3339
            "selfDeclaredMadeForKids": True,
            "defaultLanguage": lang,  # idioma da interface (legendas, título etc.)
            "defaultAudioLanguage": lang # idioma da faixa de áudio principal
        }
    }

    

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(request_body.keys()),
        body=request_body,
        # The chunksize parameter specifies the size of each chunk of data, in
        # bytes, that will be uploaded at a time. Set a higher value for
        # reliable connections as fewer chunks lead to faster uploads. Set a lower
        # value for better recovery on less reliable connections.
        #
        # Setting "chunksize" equal to -1 in the code below means that the entire
        # file will be uploaded in a single HTTP request. (If the upload fails,
        # it will still be retried where it left off.) This is usually a best
        # practice, but if you're using Python older than 2.6 or if you're
        # running on App Engine, you should set the chunksize to something like
        # 1024 * 1024 (1 megabyte).
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )
    ret_video_id = resumable_upload(youtube, insert_request)

    count = 0
    for short_file in  sorted(os.listdir(os.path.dirname(file_path))):
        if pattn_short in  short_file: 
            count = count + 1 

    for short_file in  sorted(os.listdir(os.path.dirname(file_path))):
        h = 7 # Primeira publicação as 7 horas da manha
        if pattn_short in  short_file: 
            split = pattn_short.split("_")

            # E queira adicionar uma hora (por exemplo, 14:30)
            hora = time(h, 30)
            h = h + 2

            # Combinar data + hora → datetime
            data_shot = datetime.combine(scheduled_time.date(), hora)

            request_body_short = {
                "snippet": {
                    "title": title + " - Parte "+ str(int(split[-1])+1)+ "/"+str(count) + " - #shorts",
                    "description": description,
                    "tags": tags,
                    "categoryId": "27",  # Categoria "Education"
                },
                "status": {
                    "privacyStatus": "private",  # Começa como privado
                    "publishAt": data_shot.isoformat("T") + "Z",  # Formato RFC3339
                    "selfDeclaredMadeForKids": True,
                    "defaultLanguage": lang,  # idioma da interface (legendas, título etc.)
                    "defaultAudioLanguage": lang # idioma da faixa de áudio principal
                }
            }




            # Call the API's videos.insert method to create and upload the video.
            insert_request_short = youtube.videos().insert(
                part=",".join(request_body_short.keys()),
                body=request_body_short,
                # The chunksize parameter specifies the size of each chunk of data, in
                # bytes, that will be uploaded at a time. Set a higher value for
                # reliable connections as fewer chunks lead to faster uploads. Set a lower
                # value for better recovery on less reliable connections.
                #
                # Setting "chunksize" equal to -1 in the code below means that the entire
                # file will be uploaded in a single HTTP request. (If the upload fails,
                # it will still be retried where it left off.) This is usually a best
                # practice, but if you're using Python older than 2.6 or if you're
                # running on App Engine, you should set the chunksize to something like
                # 1024 * 1024 (1 megabyte).
                media_body=MediaFileUpload(short_file, chunksize=-1, resumable=True)
            )

            resumable_upload(youtube, insert_request_short)

    
    

    return ret_video_id

    

# This method implements an exponential backoff strategy to resume a
# failed upload.

def resumable_upload(youtube,insert_request):
    response = None
    error = None
    retry = 0

    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print("✅ Vídeo enviado com sucesso! ID:", response["id"])
                    return response["id"]
                else:
                    raise Exception("Upload falhou com resposta inesperada: %s" % response)
                    return None

        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f"Erro HTTP recuperável {e.resp.status}:\n{e.content}"
            else:
                raise

        except RETRIABLE_EXCEPTIONS as e:
            error = f"Erro recuperável: {e}"

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                raise Exception("Número máximo de tentativas excedido.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print(f"⏳ Aguardando {sleep_seconds:.2f} segundos para tentar novamente...")
            time.sleep(sleep_seconds)


def get_next_tuesday_or_thursday(from_date=None):
    if from_date is None:
        from_date = datetime.today()
    elif isinstance(from_date, str):
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
    
    print(from_date)

    for i in range(1, 8):
        next_day = from_date + timedelta(days=i)
        if next_day.weekday() in [1, 3]:  # 1 = terça, 3 = quinta
            # E queira adicionar uma hora (por exemplo, 14:30)
            hora = time(14, 30)

            # Combinar data + hora → datetime
            data_completa = datetime.combine(next_day.date(), hora)
            return data_completa


def sendVideoLong(id, content_dir, agendar_para, history, lang ): 
    
    youtube = get_authenticated_service()
    if lang == 'pt':
        video_id = upload_video(youtube, content_dir+"/"+str(id)+"_multiaudio"+".mp4", history[lang]['title'], history[lang]['description'], history[lang]['tags'], agendar_para, lang,pattn_short=+str(id)+"_"+lang+"_SHORTS_")
    else:
        video_id = upload_video(youtube, content_dir+"/"+str(id)+"_"+lang+".mp4", history[lang]['title'], history[lang]['description'], history[lang]['tags'], agendar_para, lang, pattn_short=+str(id)+"_"+lang+"_SHORTS_")
    return video_id
        




def send(id, type_up, lang='pt'):
    # Buscar caminho dos conteudos
    PATH_PROJET =  interfaceUtils()
    content_dir = os.path.join(PATH_PROJET["path_youtube_video"], str(id))
    if not os.path.exists(content_dir):
        os.makedirs(content_dir)
    # CONTROLE
    with open(PATH_PROJET['historic_history'], "r", encoding="utf-8") as file:
        controle = json.load(file)
    # Historia
    with open(PATH_PROJET['path_history']+str(id)+"_history.json", "r", encoding="utf-8") as file:
        history = json.load(file)

    try:
        submits = controle['submits']
        if len(submits) == 0:
            agendar_para = get_next_tuesday_or_thursday()
        else:
            print(submits)
            agendar_para = get_next_tuesday_or_thursday(submits[-1])
    except:
        temp = []
        print(submits)
        agendar_para = get_next_tuesday_or_thursday()
        temp.append(agendar_para)
        submits = temp
        print(submits)


    if type_up == "youtube":
        try:
            video_id = sendVideoLong(id, content_dir, agendar_para, history, lang )
            stepComplete(step="youtube_complete"+lang,id=(id, video_id))
            controle['submits'] = submits.append(agendar_para)
            with open(PATH_PROJET['historic_history'], "w", encoding="utf-8") as json_file:
                json.dump(controle, json_file, indent=4, ensure_ascii=False)
        except:
            # Salva a nova data/hora da execução
            now = datetime.now().isoformat()
            controle['API_YOUTUBE'] = now
            with open(PATH_PROJET['historic_history'], "w") as f:
                json.dump(controle, f, indent=4) 

    if type_up == "youtube":
        try:
            upload_legend(content_dir, video_id, id, history, lang)
            stepComplete(step="youtube_complete"+lang,id=(id, video_id))
            controle['submits'] = submits.append(agendar_para)
            with open(PATH_PROJET['historic_history'], "w", encoding="utf-8") as json_file:
                json.dump(controle, json_file, indent=4, ensure_ascii=False)
        except:
            # Salva a nova data/hora da execução
            now = datetime.now().isoformat()
            controle['API_YOUTUBE'] = now
            with open(PATH_PROJET['historic_history'], "w") as f:
                json.dump(controle, f, indent=4) 


    

    

 
    

    

    flag_excess = False
    if flag_excess:  
        
    


# Exemplo de uso
if __name__ == "__main__":
    send("criancas_0")








