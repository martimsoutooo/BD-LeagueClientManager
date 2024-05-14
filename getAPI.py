import requests
import pyodbc
import time

def fetch_and_store_champions(api_key, connection_string):
    # Configuração da conexão com o banco de dados
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # URL para a API de campeões
    region = 'na1'
    url = f'https://{region}.api.riotgames.com/lol/static-data/v3/champions'
    params = {
        'locale': 'en_US',
        'dataById': 'false',
        'api_key': api_key
    }

    try:
        # Fazendo a requisição à API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta uma exceção para respostas 4XX e 5XX
        champions_data = response.json()['data']

        # Inserir dados na tabela Champion
        for champ_key, details in champions_data.items():
            name = details['name']
            title = details['title']  # Supondo que você também queira guardar o título
            # Supondo que 'Item_Type_ID' seja gerado automaticamente ou já conhecido/definido
            cursor.execute("INSERT INTO LCM.Champion (Name, Title) VALUES (?, ?)", (name, title))
            conn.commit()
            time.sleep(1)  # Dorme por 1 segundo para controlar a frequência de requisições

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            retry_after = int(e.response.headers['Retry-After'])
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
            fetch_and_store_champions(api_key, connection_string)  # Tenta novamente após o tempo de espera
        else:
            print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Fechando a conexão
        conn.close()

# Exemplo de uso
api_key = 'RGAPI-a347caa4-1737-40d8-b66f-b15ec1a3b51d'
connection_string = 'DRIVER={SQL Server};SERVER=your_server;DATABASE=your_database;UID=your_username;PWD=your_password'
fetch_and_store_champions(api_key, connection_string)
