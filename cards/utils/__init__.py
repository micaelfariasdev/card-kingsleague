import requests
from dotenv import load_dotenv
import os
load_dotenv()

def remove_background(input_image_path, output_image_path):
    # Obter a chave da API do remove.bg a partir do arquivo .env
    api_key = os.getenv('API_KEY')

    if not api_key:
        print("Chave da API não encontrada. Verifique o arquivo .env.")
        return

    # URL da API do remove.bg
    url = 'https://api.remove.bg/v1.0/removebg'

    # Abrindo a imagem para envio
    with open(input_image_path, 'rb') as file:
        # Enviando a requisição com a imagem e a chave da API
        response = requests.post(
            url,
            files={'image_file': file},
            data={'size': 'auto'},
            headers={'X-Api-Key': api_key},
        )

    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Salvando a imagem com fundo removido
        with open(output_image_path, 'wb') as out_file:
            out_file.write(response.content)
        print(f"Imagem salva em: {output_image_path}")
    else:
        print(f"Erro: {response.status_code} - {response.text}")
