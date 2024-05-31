import requests
import pyodbc
import random

def fetch_champion_data():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=tcp:mednat.ieeta.pt\SQLSERVER,8101;DATABASE=p11g1;UID=p11g1;PWD=RMachado@10')
    cursor = conn.cursor()
    
    version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    version = requests.get(version_url).json()[0]
    
    champions_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    response = requests.get(champions_url)
    champions_data = response.json()['data']
    
    # Convert the champions_data dictionary to a list and shuffle it
    champions_list = list(champions_data.items())
    random.shuffle(champions_list)
    
    for champion_key, champion_info in champions_list:
        champion_name = champion_info['name']
        
        # Verifica se o item já está inserido na tabela Item
        cursor.execute("SELECT COUNT(*) FROM LCM.Item WHERE Name = ? AND Type = 'Champion'", (champion_name,))
        if cursor.fetchone()[0] == 0:
            first_tag = champion_info['tags'][0] if champion_info['tags'] else 'Unknown'
            
            detailed_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{champion_key}.json"
            detailed_response = requests.get(detailed_url).json()
            detailed_info = detailed_response['data'][champion_key]
            
            lore = detailed_info['lore']
            kingdom = extract_kingdom_from_lore(lore)
            be_price = 1350
            
            # Insere dados na tabela Item
            cursor.execute("INSERT INTO LCM.Item (Name, Type, BE_Price) OUTPUT INSERTED.ID VALUES (?, 'Champion', ?)",
                           (champion_name, be_price))
            item_id = cursor.fetchone()[0]
            
            # Insere dados na tabela Champion
            cursor.execute("INSERT INTO LCM.Champion (ID, Name, BE_Price, Category, Kingdom) VALUES (?, ?, ?, ?, ?)",
                           (item_id, champion_name, be_price, first_tag, kingdom))
            conn.commit()
            print(f"Champion {champion_name} inserted successfully.")
        else:
            print(f"Champion {champion_name} already exists in the database.")

    conn.close()

def extract_kingdom_from_lore(lore):
    possible_kingdoms = ['Demacia', 'Noxus', 'Freljord', 'Piltover', 'Zaun', 'Ionia', 'Shurima', 'Targon', 'Bilgewater', 'Shadow Isles', 'Unknown']
    for kingdom in possible_kingdoms:
        if kingdom in lore:
            return kingdom
    return "Unknown"

fetch_champion_data()
