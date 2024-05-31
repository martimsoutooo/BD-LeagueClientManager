import random
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from ..data.models import purchaseRP
from ..data.database import get_db

main_bp = Blueprint('main', __name__)

# já vi
@main_bp.route('/')
def index():
    return render_template('login.html')
# já vi
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

        cursor.execute("SELECT Rank_Points, RP, BE, Rank FROM GetUserInfo(?)", (user_id,))
        info = cursor.fetchone()

        user_rank_points = info.Rank_Points
        user_rp = info.RP
        user_be = info.BE
        user_rank = info.Rank

        cursor.execute("SELECT * FROM GetChampionsByUser(?)", (user_id,))
        champions = cursor.fetchall()

        cursor.execute("SELECT * FROM GetWardsByUser(?)", (user_id,))
        wards = cursor.fetchall()

        cursor.execute("SELECT ID, Name FROM LCM.Map")
        maps = cursor.fetchall()

        return render_template('game.html', user_rank_points=user_rank_points, user_rp=user_rp, user_be=user_be,
                               champions=champions, wards=wards, maps=maps, user_rank=user_rank)
    
    elif request.method == 'POST':
        data = request.get_json()
        champion_id = data['champion_id']
        skin_id = data.get('skin_id')
        ward_id = data['ward_id']
        map_id = data['map_id']

        try:
            cursor.execute("EXEC sp_InsertUserSelection @UserID=?, @SkinID=?, @ChampionID=?, @WardID=?",
                           (user_id, skin_id, champion_id, ward_id))
            user_select_id = cursor.fetchone()[0]
            db.commit()

            cursor.execute("EXEC sp_StartGame @ID_Map=?, @ID_User_Select=?", (map_id, user_select_id))
            db.commit()

            cursor.execute("SELECT Result, Duration, Outcome_RP, Outcome_BE FROM LCM.Game WHERE ID_User_Select=?", (user_select_id,))
            game_result = cursor.fetchone()
            return jsonify({"status": "success", "message": "Game started successfully", "game": {
                "Result": game_result[0],
                "Duration": game_result[1],
                "Outcome_RP": game_result[2],
                "Outcome_BE": game_result[3]
            }})
        
        except Exception as e:
            db.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500
        
        

@main_bp.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        print("User ID not found in session")
        return redirect(url_for('auth.login'))
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM GetUserInfo(?)", user_id)
    info = cursor.fetchone()

    user_be = info.BE
    user_rp = info.RP
    user_rank = info.Rank

    cursor.execute("""
        SELECT *
        FROM LCM.View_UserGameHistory ui
        WHERE ui.ID_User = (?)
    """, (user_id,))
    game_history = cursor.fetchall()

    cursor.execute("""
        SELECT *
        FROM LCM.View_UserBuyHistory ui
        JOIN LCM.Item i ON ui.ID_Item = i.ID
        WHERE ui.ID_User = (?)
    """, (user_id,))
    purchase_history = cursor.fetchall()

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
                           chest_quantities=chest_quantities,
                           user_rank=user_rank,
                           game_history=game_history,
                           purchase_history=purchase_history
                           )


@main_bp.route('/store')
def store():
    user_id = session.get('user_id')
    if not user_id:
        print("User ID not found in session")
        return redirect(url_for('auth.login'))
    
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM GetUserInfo(?)", user_id)
    info = cursor.fetchone()

    user_be = info.BE
    user_rp = info.RP

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
    
    db = get_db()
    cursor = db.cursor()

    cursor.execute("EXEC BuyChampion ?, ?, ?", (user_id, champion_id, be_price))
    result = cursor.fetchone()
    db.commit()

    if result and result.Result == 'Success':
        return {"status": "success", "message": result.Message}
    else:
        return {"status": "error", "message": result.Message}


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
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("EXEC BuySkin ?, ?, ?", (user_id, skin_id, rp_price))
    result = cursor.fetchone()
    db.commit()

    if result and result.Result == 'Success':
        return {"status": "success", "message": result.Message}
    else:
        return {"status": "error", "message": result.Message}


@main_bp.route('/buy_ward_route', methods=['POST'])
def buy_ward_route():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401

    data = request.get_json()
    ward_id = data.get('ward_id')
    rp_price = data.get('rp_price')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("EXEC BuyWard ?, ?, ?", (user_id, ward_id, rp_price))
    result = cursor.fetchone()
    db.commit()

    if result and result[0] == 'Success':
        return {"status": "success", "message": result[1]}
    else:
        return {"status": "error", "message": result[1] if result else "Unknown error occurred"}


@main_bp.route('/buy_chest_route', methods=['POST'])
def buy_chest_route():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Not logged in"}), 401

    data = request.get_json()
    chest_id = data.get('chest_id')
    rp_price = data.get('rp_price')
    chest_type = data.get('chest_type')

    if 'Skin' in chest_type:
        chest_type = 'Skin'
    elif 'Champion' in chest_type:
        chest_type = 'Champion'
    elif 'Ward' in chest_type:
        chest_type = 'Ward'

    db = get_db()
    cursor = db.cursor()
    cursor.execute("EXEC BuyChest ?, ?, ?, ?", (user_id, chest_id, rp_price, chest_type))
    result = cursor.fetchone()
    db.commit()

    if result and result[0] == 'Success':
        return {"status": "success", "message": result[1]}
    else:
        return {"status": "error", "message": result[1] if result else "Unknown error occurred"}


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


@main_bp.route('/filter_data')
def filter_data():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify([])

    data_type = request.args.get('type', 'Champion')
    alphabetical = request.args.get('alphabetical', '0')
    kingdom = request.args.get('kingdom', 'all')
    category = request.args.get('category', 'all')

    if alphabetical == 'on':
        alphabetical = 1
    else:
        alphabetical = 0

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        EXEC GetFilteredData @UserID=?, @Type=?, @Alphabetical=?, @Filter1=?, @Filter2=?
    """, (user_id, data_type, alphabetical, kingdom, category))
    
    if data_type == 'Champion':
        columns = ['ID', 'Name', 'Category', 'Kingdom']
    elif data_type == 'Skin':
        columns = ['ID', 'skin', 'championName']
    elif data_type == 'Ward':
        columns = ['ID', 'ward']

    result = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    if data_type == 'Champion':
        return render_template('partials/_profile_champion_list.html', champions=result)
    elif data_type == 'Skin':
        print(result)
        return render_template('partials/_profile_skin_list.html', skins=result)
    elif data_type == 'Ward':
        return render_template('partials/_profile_ward_list.html', wards=result)
    
    return jsonify([])

@main_bp.route('/filter_data_store')
def filter_data_store():

    user_id = session.get('user_id')
    if not user_id:
        return jsonify([])
    
    data_type = request.args.get('type', 'Champion')
    alphabetical = request.args.get('alphabetical', '0')
    kingdom = request.args.get('kingdom', 'all')
    category = request.args.get('category', 'all')

    if alphabetical == 'on':
        alphabetical = 1
    else:
        alphabetical = 0

    print(alphabetical)

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        EXEC GetFilteredDataStore @UserID=?, @Type=?, @Alphabetical=?, @Filter1=?, @Filter2=?
    """, (user_id, data_type, alphabetical, kingdom, category))

    if data_type == 'Champion':
        columns = ['ID', 'Name', 'Category', 'BE_Price','Kingdom']
    elif data_type == 'Skin':
        columns = ['ID', 'skin', 'champion', 'rp_price']
    elif data_type == 'Ward':
        columns = ['ID', 'Name', 'rp_price']

    result = [dict(zip(columns, row)) for row in cursor.fetchall()]


    if data_type == 'Champion':
        return render_template('partials/_store_champion_list.html', champions=result)
    elif data_type == 'Skin':
        print(result)
        return render_template('partials/_store_skin_list.html', skins=result)
    elif data_type == 'Ward':
        print(result)
        return render_template('partials/_store_ward_list.html', wards=result)
    
    return jsonify([])

@main_bp.route('/search_champions', methods=['GET'])
def search_champions():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify([])

    search_query = request.args.get('query', '')
    max_results = int(request.args.get('max_results', 50))

    db = get_db()
    cursor = db.cursor()

    cursor.execute("EXEC SearchChampions @UserID=?, @SearchQuery=?, @MaxResults=?", (user_id, search_query, max_results))
    champions = cursor.fetchall()

    champion_list = [{'ID': champ[0], 'Name': champ[1], 'Category': champ[2], 'BE_Price': champ[3], 'Kingdom': champ[4]} for champ in champions]
    
    return jsonify(champions=champion_list)

@main_bp.route('/search_skins', methods=['GET'])
def search_skins():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify([])

    search_query = request.args.get('query', '')
    max_results = int(request.args.get('max_results', 50))

    db = get_db()
    cursor = db.cursor()

    cursor.execute("EXEC SearchSkins @UserID=?, @SearchQuery=?, @MaxResults=?", (user_id, search_query, max_results))
    skins = cursor.fetchall()

    skin_list = [{'ID': skin[0], 'Skin': skin[1], 'Champion': skin[2], 'RP_Price': skin[3]} for skin in skins]
    
    return jsonify(skins=skin_list)



