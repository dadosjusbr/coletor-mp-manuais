from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import csv
import sys
from dotenv import load_dotenv
import json

load_dotenv()


# ID da pasta que contém todas as planilhas a serem listas
if "DATA_FOLDER_ID" in os.environ:
    DATA_FOLDER_ID = os.environ["DATA_FOLDER_ID"]
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'DATA_FOLDER_ID'.\n")
    os._exit(1)

# ID da lista que será atualizada no drive
if "FILE_ID" in os.environ:
    FILE_ID = os.environ["FILE_ID"]
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'FILE_ID'.\n")
    os._exit(1)

if not os.path.exists("./credentials.json"):
    if "CREDENTIALS" in os.environ:
        credentials = os.environ["CREDENTIALS"]
        credentials = json.loads(credentials)

        with open(f"credentials.json", "w", encoding="utf-8") as arquivo:
            json.dump(credentials, arquivo, ensure_ascii=False, indent=4)
    else:
        sys.stderr.write("Invalid arguments, missing parameter: 'CREDENTIALS'.\n")
        os._exit(1)
    
# Autentica usando as credenciais da conta de serviço
creds = service_account.Credentials.from_service_account_file(
    "credentials.json", scopes=["https://www.googleapis.com/auth/drive"]
)

# Conecta-se à API do Google Drive
service = build("drive", "v3", credentials=creds)


def list_folders():
    folders = []
    page_token = None

    # Listar ID das pastas (de cada órgão) dentro da pasta especificada
    while True:
        results = (
            service.files()
            .list(
                q=f"'{DATA_FOLDER_ID}' in parents",
                pageSize=100,
                fields="nextPageToken, files(id)",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
                pageToken=page_token,
            )
            .execute()
        )

        folders.extend(results.get("files", []))
        page_token = results.get("nextPageToken", None)

        if not page_token:
            break

    if not folders:
        print("Pasta não encontrada.")
        os._exit(1)
    else:
        return folders


def list_files(folders):
    files = []
    for folder in folders:
        page_token = None

        while True:
            results = (
                service.files()
                .list(
                    q=f"'{folder['id']}' in parents",
                    pageSize=100,
                    fields="nextPageToken, files(id, name, createdTime)",
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                    pageToken=page_token,
                )
                .execute()
            )

            files.extend(results.get("files", []))
            page_token = results.get("nextPageToken", None)

            if not page_token:
                break

    return files


def create_csv(files):
    list_path = "lista_planilhas_baixadas.csv"
    with open(list_path, mode="w", newline="", encoding="utf-8") as csv_list:
        csv_writer = csv.writer(csv_list)

        # Criando o cabeçalho
        csv_writer.writerows([["orgao", "mes", "ano", "arquivo", "id_arquivo", "data"]])

        for file in files:
            # @old é o nome da pasta criada para armazenar planilhas "velhas",
            # i.e. que foram baixadas, mas estavam quebradas/erradas e foram armazenadas novas 
            if file['name'] != '@old':
                # removendo a extensão
                filename = os.path.splitext(file["name"])[0]

                # Dividir a string pelo delimitador '-'
                parts = filename.split("-")

                orgao = parts[0].lower()
                mes = parts[2]
                ano = parts[3]

                csv_writer.writerows(
                    [[orgao, mes, ano, file["name"], file["id"], file["createdTime"]]]
                )

    return list_path


def upload_list(list_path):
    # Armazenando o csv no drive
    file_name = os.path.basename(list_path)

    # Upload do arquivo
    media = MediaFileUpload(list_path, mimetype="text/csv")
    file = (
        service.files()
        .update(fileId=FILE_ID, media_body=media, supportsAllDrives=True)
        .execute()
    )


if __name__ == "__main__":
    folders = list_folders()
    files = list_files(folders)
    list_path = create_csv(files)
    upload_list(list_path)
