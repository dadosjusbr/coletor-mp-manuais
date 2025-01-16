# Coletor MPs Manuais

Este coletor possui 2 funções:

1. Criar e atualizar listagem de arquivos no drive (planilhas de contracheques e indenizações coletados manualmente)
2. Realizar o download dos arquivos do órgão/ano/mês de referência dentro do pipeline de coleta (no qual os dados serão tratados, padronizados e armazenados).

## Variáveis de ambiente e arquivos necessários

As variáveis de ambiente poderão ser passadas pelo próprio comando, e.g. `FILE_ID={} python3...` ou por um arquivo .env.

- `credentials.json`: arquivo .json contendo as credenciais da conta de serviço.
- `DATA_FOLDER_ID`: ID da pasta no drive no qual estão armazenadas as pastas de dados de cada órgão.
- `FILE_ID`: ID do arquivo no drive (lista_planilhas_baixadas.csv). O arquivo será atualizado e também utilizado para consultar os arquivos durante o pipeline de coleta.

## Antes de tudo...

Crie um ambiente virtual e baixe os pacotes necessários:

```{sh}
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Como atualizar a lista de arquivos

```{sh}
python3 src/list_drive_files.py
```

## Como fazer o download dos arquivos

Passamos como parâmetro `COURT`, `MONTH`, `YEAR` e `OUTPUT_FOLDER`, i.e. órgão, ano e mês de referência e diretório no qual os arquivos serão armazenados, respectivamente.

```{sh}
COURT=MPPA MONTH=06 YEAR=2022 OUTPUT_FOLDER=. python3 src/main.py
```
