import requests
import pyodbc

def fetch_champion_data():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=LeagueClientManager;Trusted_Connection=yes;')
    cursor = conn.cursor()
    
    version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    version = requests.get(version_url).json()[0]
    
    champions_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    response = requests.get(champions_url)
    champions_data = response.json()['data']
    
    for champion_key, champion_info in champions_data.items():
        champion_id = int(champion_info['key'])
        champion_name = champion_info['name']  # Define 'champion_name' fora do bloco if para acesso universal
        
        # Verifica se o campeão já está inserido na tabela Champion
        cursor.execute("SELECT COUNT(*) FROM LCM.Champion WHERE ID_Item_Type = ?", (champion_id,))
        if cursor.fetchone()[0] == 0:
            first_tag = champion_info['tags'][0] if champion_info['tags'] else 'Unknown'
            
            detailed_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{champion_key}.json"
            detailed_response = requests.get(detailed_url).json()
            detailed_info = detailed_response['data'][champion_key]
            
            lore = detailed_info['lore']
            kingdom = extract_kingdom_from_lore(lore)
            be_price = 1350
            
            # Insere em Item_Type se necessário
            cursor.execute("SELECT COUNT(*) FROM LCM.Item_Type WHERE ID = ?", (champion_id,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO LCM.Item_Type (ID, Name, RP_Price) VALUES (?, ?, ?)",
                               (champion_id, champion_name, None))
            
            # Insere dados na tabela Champion
            cursor.execute("INSERT INTO LCM.Champion (ID_Item_Type, Name, BE_Price, Category, Kingdom) VALUES (?, ?, ?, ?, ?)",
                           (champion_id, champion_name, be_price, first_tag, kingdom))
            conn.commit()
        else:
            print(f"Champion {champion_name} already exists in the database.")

    conn.close()

def extract_kingdom_from_lore(lore):
    possible_kingdoms = ['Demacia', 'Noxus', 'Freljord', 'Piltover', 'Zaun', 'Ionia', 'Shurima', 'Targon', 'Bilgewater', 'Shadow Isles']
    for kingdom in possible_kingdoms:
        if kingdom in lore:
            return kingdom
    return "Unknown"

fetch_champion_data()






