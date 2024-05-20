import pyodbc
from .database import get_db

def create_user(username, email, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("EXEC CreateUser ?, ?, ?", (username, email, password))
    db.commit()

def get_user_by_username(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM LCM.[User] WHERE Name = ?", (username,))
    user = cursor.fetchone()
    return user

def get_user_by_email(email):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM LCM.[User] WHERE Email = ?", (email,))
    user = cursor.fetchone()
    return user

def verify_user(username, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("EXEC VerifyUser ?, ?", (username, password))
    user = cursor.fetchone()
    return user

def buy_champion(user_id, champion_id, be_price):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("EXEC BuyChampion ?, ?, ?", (user_id, champion_id, be_price))
    result = cursor.fetchone()
    db.commit()
    
    if result and result.Result == 'Success':
        return {"status": "success", "message": result.Message}
    else:
        return {"status": "error", "message": result.Message}

def buy_skin(user_id, skin_id, rp_price):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("EXEC BuySkin ?, ?, ?", (user_id, skin_id, rp_price))
    result = cursor.fetchone()
    db.commit()

    if result and result.Result == 'Success':
        return {"status": "success", "message": result.Message}
    else:
        return {"status": "error", "message": result.Message}



def get_user_balance(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM GetUserBalance(?)", user_id)
    balance = cursor.fetchone()
    return balance








