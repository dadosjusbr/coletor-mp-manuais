import sys
import os
import crawler
import json
from google.oauth2 import service_account


if "COURT" in os.environ:
    court = os.environ["COURT"].casefold()
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'COURT'.\n")
    os._exit(1)

if "YEAR" in os.environ:
    year = int(os.environ["YEAR"])
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'YEAR'.\n")
    os._exit(1)

if "MONTH" in os.environ:
    month = int(os.environ["MONTH"])
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'MONTH'.\n")
    os._exit(1)

if "OUTPUT_FOLDER" in os.environ:
    output_path = os.environ["OUTPUT_FOLDER"]
else:
    output_path = "./output"
    
if "CREDENTIALS" in os.environ:
    credentials = os.environ["CREDENTIALS"]
    credentials = json.loads(credentials)

    with open(f"{output_path}/credentials.json", "w", encoding="utf-8") as arquivo:
        json.dump(credentials, arquivo, ensure_ascii=False, indent=4)
        
    # Autentica usando as credenciais da conta de serviço
    creds = service_account.Credentials.from_service_account_file(
        "credentials.json", scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'CREDENTIALS'.\n")
    os._exit(1)
    
# ID da lista no drive, referente às planilhas baixadas manualmente
if "FILE_ID" in os.environ:
    file_id = os.environ["FILE_ID"]
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'FILE_ID'.\n")
    os._exit(1)
    
# Baixamos a lista de arquivos
crawler.download_list(file_id, creds)

# Consultamos se os arquivos existem
result = crawler.consult_list(court, month, year)

# Baixamos os arquivos
stdout = crawler.download_files(output_path, result, creds)

# Retornamos o timestamp e o caminho dos arquivos
print('\n'.join(stdout))
