import requests
import pyodbc

def fetch_champion_data():
    # Estabelece conexão com o banco de dados
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=LeagueClientManager;Trusted_Connection=yes;')
    cursor = conn.cursor()
    
    version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    version = requests.get(version_url).json()[0]
    
    champions_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    response = requests.get(champions_url)
    champions_data = response.json()['data']
    
    for champion_key, champion_info in champions_data.items():
        champion_id = int(champion_info['key'])
        champion_name = champion_info['name']
        
        # Verifica se o campeão já está inserido na tabela Item
        cursor.execute("SELECT ID FROM LCM.Item WHERE Name = ? AND Type = 'Champion'", (champion_name,))
        item_row = cursor.fetchone()
        
        if item_row:
            item_id = item_row[0]
            # Chama a função para buscar e inserir skins para cada campeão
            fetch_and_insert_skins(cursor, champion_key, item_id, version)
        else:
            print(f"Champion {champion_name} not found in Item table.")
    
    conn.close()

def fetch_and_insert_skins(cursor, champion_key, item_id, version):
    skins_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{champion_key}.json"
    response = requests.get(skins_url).json()
    skins_data = response['data'][champion_key]['skins']  # Obtém dados das skins
    
    for skin in skins_data:
        skin_id = int(skin['id'])
        name = skin['name']
        rp_price = 450  # RP_Price pré-definido como 450 para todas as skins
        
        # Verifica se a skin já está inserida na tabela Skin
        cursor.execute("SELECT COUNT(*) FROM LCM.Skin WHERE ID = ?", (skin_id,))
        if cursor.fetchone()[0] == 0:
            # Insere os dados na tabela Item
            cursor.execute("INSERT INTO LCM.Item (Name, Type, RP_Price) OUTPUT INSERTED.ID VALUES (?, 'Skin', ?)",
                           (name, rp_price))
            new_item_id = cursor.fetchone()[0]
            
            # Insere os dados de skin na tabela Skin
            cursor.execute("INSERT INTO LCM.Skin (ID, Champion_ID, RP_Price, Name) VALUES (?, ?, ?, ?)",
                           (new_item_id, item_id, rp_price, name))
            cursor.commit()
            print(f"Skin {name} inserted successfully.")
        else:
            print(f"Skin {name} with ID {skin_id} already exists in the database.")

fetch_champion_data()


