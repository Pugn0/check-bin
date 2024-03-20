import os
import glob
import requests
from urllib.parse import quote

def disable_ssl_warnings():
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def save_info(info, country, flag):
    dir_path = os.path.join(country)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, f'{flag}.txt')
    with open(file_path, 'a+') as arquivo:
        arquivo.write(f'{info}\n')

def call_api(info):
    headers = {
        'Host': 'farpytechsolutions.online'
    }
    url = f'https://farpytechsolutions.online/bin/{quote(info)}'
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        obj = response.json()
        save_info(info, obj['data']['country'], obj['data']['flag'])

def process_file(file_path):
    print(f"Processando o arquivo: {file_path}")
    with open(file_path, 'r') as arquivo:
        for linha in arquivo:
            call_api(linha.strip())

def choose_file(arquivos_txt):
    print("Selecione um arquivo para processar:")
    for idx, arquivo in enumerate(arquivos_txt, start=1):
        print(f"{idx}. {arquivo}")
    escolha = int(input("Digite o número do arquivo: ")) - 1
    return arquivos_txt[escolha]

def main():
    disable_ssl_warnings()
    diretorio = "DB"
    arquivos_txt = glob.glob(os.path.join(diretorio, "*.txt"))

    if not arquivos_txt:
        print("Não foram encontrados arquivos .txt no diretório especificado.")
        return

    arquivo_selecionado = choose_file(arquivos_txt)
    try:
        process_file(arquivo_selecionado)
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo {arquivo_selecionado}: {e}")

if __name__ == "__main__":
    main()
