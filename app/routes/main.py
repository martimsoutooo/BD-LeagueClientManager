import random
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from ..data.models import buy_champion, buy_skin, get_user_balance, buy_ward, buy_chest,purchaseRP
from ..data.database import get_db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('login.html')

@main_bp.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        print("User ID not found in session")
        return redirect(url_for('auth.login'))
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT Name FROM LCM.[User] WHERE ID = ?", (user_id,))
    user_name = cursor.fetchone()[0]

    return render_template('dashboard.html', user_name=user_name)

@main_bp.route('/game', methods=['GET', 'POST'])
def game():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    db = get_db()
    cursor = db.cursor()

    if request.method == 'GET':
        # Carrega dados iniciais para a tela de seleção de jogo
        cursor.execute("SELECT * FROM GetUserInfo(?)", (user_id,))
        user_data = cursor.fetchone()
        user_rank_points, user_rp = (user_data or (None, None))

        cursor.execute("SELECT * FROM GetUserChampions(?)", (user_id,))
        champions = cursor.fetchall()
        cursor.execute("SELECT * FROM GetUserWards(?)", (user_id,))
        wards = cursor.fetchall()
        cursor.execute("SELECT ID, Name FROM LCM.Map")
        maps = cursor.fetchall()

        return render_template('game.html', user_rank_points=user_rank_points, user_rp=user_rp,
                               champions=champions, wards=wards, maps=maps)
    
    elif request.method == 'POST':
        # Recebe os dados do formulário quando o usuário clica em "Start Game"
        data = request.get_json()
        champion_id = data.get('champion_id')
        skin_id = data.get('skin_id', None)  # Pode ser None se nenhuma skin for selecionada
        ward_id = data.get('ward_id')
        map_id = data.get('map_id')

        try:
            # Insere a seleção do usuário e inicia o jogo
            cursor.execute("""
                EXEC sp_InsertUserSelection @UserID=?, @SkinID=?, @ChampionID=?, @WardID=?""",
                (user_id, skin_id, champion_id, ward_id))
            user_select_id = cursor.fetchone()[0]
            db.commit()

            cursor.execute("""
                EXEC sp_StartGame @ID_Map=?, @ID_User_Select=?""",
                (map_id, user_select_id))
            db.commit()

            return jsonify({"status": "success", "message": "Game started successfully"})
        except Exception as e:
            db.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500
        
        

@main_bp.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        print("User ID not found in session")
        return redirect(url_for('auth.login'))
    
    balance = get_user_balance(user_id)
    user_be = balance.BE
    user_rp = balance.RP
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT ID, Name, Category, Kingdom FROM GetChampionsByUser(?)", (user_id,))
    champions = cursor.fetchall()

    cursor.execute("SELECT ID, skin, championName FROM GetSkinsByUser(?)", (user_id,))
    skins = cursor.fetchall()

    cursor.execute("SELECT ID, ward FROM GetWardsByUser(?)", (user_id,))
    wards = cursor.fetchall()

    cursor.execute("SELECT ID, chest FROM GetChestsByUser(?)", (user_id,))
    chests = cursor.fetchall()

    # Fetch chest quantities
    cursor.execute("SELECT chestsSkin_qty, chestsChampion_qty, chestsWard_qty FROM LCM.[User] WHERE ID = ?", (user_id,))
    chest_quantities = cursor.fetchone()
    
    return render_template('profile.html', 
                           champions=champions, 
                           skins=skins, 
                           wards=wards, 
                           chests=chests,
                           user_be=user_be, 
                           user_rp=user_rp,
                           chest_quantities=chest_quantities)


@main_bp.route('/store')
def store():
    user_id = session.get('user_id')
    if not user_id:
        print("User ID not found in session")
        return redirect(url_for('auth.login'))
    
    balance = get_user_balance(user_id)
    user_be = balance.BE
    user_rp = balance.RP
    
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT ID, Name, Category, BE_Price, Kingdom FROM GetAvailableChampionsForUser(?)",(user_id))
    champions = cursor.fetchall()

    cursor.execute("SELECT ID, skin, champion, rp_price FROM GetAvailableSkinsForUser(?)",(user_id))
    skins = cursor.fetchall()

    cursor.execute("SELECT Name, ID, rp_price FROM GetAvailableWardsForUser(?)", (user_id))
    wards = cursor.fetchall()

    cursor.execute("SELECT ID, Name, rp_price FROM dbo.GetChestsAndPrices()")
    chests = cursor.fetchall()

    return render_template('store.html', champions=champions, skins=skins, wards=wards, chests=chests, user_be=user_be, user_rp=user_rp)


@main_bp.route('/buy_champion_route', methods=['POST'])
def buy_champion_route():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401

    data = request.get_json()
    champion_id = data.get('champion_id')
    be_price = data.get('be_price')
    
    result = buy_champion(user_id, int(champion_id), int(be_price))
    return jsonify(result)


@main_bp.route('/purchase_rp', methods=['POST'])
def purchase_rp():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401
    
    data = request.get_json()
    rp_amount = data.get('rp_amount')
    
    if not rp_amount or int(rp_amount) <= 0:
        return jsonify({"status": "error", "message": "Invalid amount"}), 400
    
    purchaseRP(user_id,rp_amount)
    return jsonify({"status": "success", "message": f"{rp_amount} RP added successfully"})


@main_bp.route('/buy_skin_route', methods=['POST'])
def buy_skin_route():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401
    
    data = request.get_json()
    skin_id = data.get('skin_id')
    rp_price = data.get('rp_price')
    
    result = buy_skin(user_id, skin_id, rp_price)
    return jsonify(result)


@main_bp.route('/buy_ward_route', methods=['POST'])
def buy_ward_route():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401

    data = request.get_json()
    ward_id = data.get('ward_id')
    rp_price = data.get('rp_price')

    result = buy_ward(user_id, ward_id, rp_price)
    return jsonify(result)


@main_bp.route('/buy_chest_route', methods=['POST'])
def buy_chest_route():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401

    data = request.get_json()
    chest_id = data.get('chest_id')
    rp_price = data.get('rp_price')
    chest_type = data.get('chest_type')

    print('Ola')
    print(chest_type)

    result = buy_chest(user_id, chest_id, rp_price,chest_type)
    return jsonify(result)


@main_bp.route('/selectSkin/<int:champion_id>', methods=['GET'])
def select_skin(champion_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT S.ID, S.Name AS skin_name, C.Name AS champion_name
            FROM LCM.Skin S
            JOIN LCM.Champion C ON S.Champion_ID = C.ID
            JOIN LCM.User_Item UI ON S.ID = UI.ID_Item
            WHERE S.Champion_ID = ? AND UI.ID_User = ?
        """, (champion_id, user_id))
        skins = cursor.fetchall()

        skins_list = [{'id': skin[0], 'skin_name': skin[1], 'champion_name': skin[2]} for skin in skins]
        return jsonify(skins_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/open_chest/<chest_type>', methods=['POST'])
def open_chest(chest_type):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401

    db = get_db()
    cursor = db.cursor()

    # Função auxiliar para selecionar um item aleatório que o usuário ainda não possui
    def get_random_item_not_owned(query, user_id):
        cursor.execute(query, (user_id,))
        items = cursor.fetchall()
        if not items:
            return None
        return random.choice(items)

    # Check and decrement chest quantity based on chest_type
    if chest_type == 'Skin':
        cursor.execute("SELECT chestsSkin_qty FROM LCM.[User] WHERE ID = ?", (user_id,))
        current_qty = cursor.fetchone()[0]
        if current_qty > 0:
            cursor.execute("UPDATE LCM.[User] SET chestsSkin_qty = chestsSkin_qty - 1 WHERE ID = ?", (user_id,))
            item = get_random_item_not_owned("SELECT ID, Name FROM LCM.Skin WHERE ID NOT IN (SELECT ID_Item FROM LCM.User_Item WHERE ID_User = ?) AND Name <> 'default'", user_id)
            if item:
                cursor.execute("INSERT INTO LCM.User_Item (ID_User, ID_Item, Data, Hora) VALUES (?, ?, GETDATE(), GETDATE())", (user_id, item[0]))
                db.commit()
                return jsonify({"status": "success", "message": f"Skin Chest opened successfully, you won {item[1]}"})
            else:
                return jsonify({"status": "error", "message": "No available skins to win"}), 400
        else:
            return jsonify({"status": "error", "message": "No Skin Chests available"}), 400
    elif chest_type == 'Champion':
        cursor.execute("SELECT chestsChampion_qty FROM LCM.[User] WHERE ID = ?", (user_id,))
        current_qty = cursor.fetchone()[0]
        if current_qty > 0:
            cursor.execute("UPDATE LCM.[User] SET chestsChampion_qty = chestsChampion_qty - 1 WHERE ID = ?", (user_id,))
            item = get_random_item_not_owned("SELECT ID, Name FROM LCM.Champion WHERE ID NOT IN (SELECT ID_Item FROM LCM.User_Item WHERE ID_User = ?)", user_id)
            if item:
                cursor.execute("INSERT INTO LCM.User_Item (ID_User, ID_Item, Data, Hora) VALUES (?, ?, GETDATE(), GETDATE())", (user_id, item[0]))
                db.commit()
                return jsonify({"status": "success", "message": f"Champion Chest opened successfully, you won {item[1]}"})
            else:
                return jsonify({"status": "error", "message": "No available champions to win"}), 400
        else:
            return jsonify({"status": "error", "message": "No Champion Chests available"}), 400
    elif chest_type == 'Ward':
        cursor.execute("SELECT chestsWard_qty FROM LCM.[User] WHERE ID = ?", (user_id,))
        current_qty = cursor.fetchone()[0]
        if current_qty > 0:
            cursor.execute("UPDATE LCM.[User] SET chestsWard_qty = chestsWard_qty - 1 WHERE ID = ?", (user_id,))
            item = get_random_item_not_owned("SELECT ID, Name FROM LCM.Ward WHERE ID NOT IN (SELECT ID_Item FROM LCM.User_Item WHERE ID_User = ?)", user_id)
            if item:
                cursor.execute("INSERT INTO LCM.User_Item (ID_User, ID_Item, Data, Hora) VALUES (?, ?, GETDATE(), GETDATE())", (user_id, item[0]))
                db.commit()
                return jsonify({"status": "success", "message": f"Ward Chest opened successfully, you won {item[1]}"})
            else:
                return jsonify({"status": "error", "message": "No available wards to win"}), 400
        else:
            return jsonify({"status": "error", "message": "No Ward Chests available"}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid chest type"}), 400


