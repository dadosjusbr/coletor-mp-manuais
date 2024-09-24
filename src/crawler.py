from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import pandas as pd
import os
import pathlib

STATUS_DATA_UNAVAILABLE = 4

# Caminho para o arquivo JSON da conta de serviço
SERVICE_ACCOUNT_FILE = "credentials.json"

# Escopos necessários para acessar o Google Drive
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Autentica usando as credenciais da conta de serviço
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)


def download_list(file_id):
    # Conecta-se à API do Google Drive
    service = build("drive", "v3", credentials=creds)

    file_name = "lista_planilhas_baixadas.csv"

    request = service.files().get_media(fileId=file_id, supportsAllDrives=True)

    fh = io.FileIO(file_name, "wb")
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()


def consult_list(orgao, mes, ano):
    sheets_list = pd.read_csv("lista_planilhas_baixadas.csv")
    filter_list = sheets_list[
        (sheets_list.orgao == orgao)
        & (sheets_list.mes == mes)
        & (sheets_list.ano == ano)
    ]

    # Se os arquivos referentes ao órgão/mês/ano não existirem, retornamos status 4
    if filter_list.empty:
        os._exit(STATUS_DATA_UNAVAILABLE)

    return filter_list


def download_files(output_path, filter_list):
    # Pegamos a data e hora que o primeiro arquivo, do respectivo órgão/mês/ano, foi armazenado
    timestamp = filter_list.data.min()
    ts_files = [timestamp]

    # Cria diretório, se não houver
    pathlib.Path(output_path).mkdir(exist_ok=True)

    # Conecta-se à API do Google Drive
    service = build("drive", "v3", credentials=creds)

    for row in filter_list.to_numpy():
        # ID do arquivo
        file_id = row[4]

        # Nome para salvar o arquivo localmente
        file_name = output_path + "/" + row[3]

        ts_files.append(file_name)

        # Solicitar o arquivo da API do Google Drive
        request = service.files().get_media(fileId=file_id, supportsAllDrives=True)

        # Fazer o download do arquivo
        fh = io.FileIO(file_name, "wb")
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

    return ts_files
