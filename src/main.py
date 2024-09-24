import sys
import os
import crawler


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
    
# ID da lista no drive, referente às planilhas baixadas manualmente
if "FILE_ID" in os.environ:
    file_id = os.environ["FILE_ID"]
else:
    sys.stderr.write("Invalid arguments, missing parameter: 'FILE_ID'.\n")
    os._exit(1)
    
# Baixamos a lista de arquivos
crawler.download_list(file_id)

# Consultamos se os arquivos existem
result = crawler.consult_list(court, month, year)

# Baixamos os arquivos
stdout = crawler.download_files(output_path, result)

# Retornamos o timestamp e o caminho dos arquivos
print('\n'.join(stdout))
