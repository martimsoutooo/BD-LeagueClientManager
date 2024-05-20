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
    
    # Execute the stored procedure and fetch the result
    cursor.execute("EXEC BuyChampion ?, ?, ?", (user_id, champion_id, be_price))
    result = cursor.fetchone()
    
    # Add logs for debugging
    print("Stored procedure result:", result)
    
    # Check if the result is not None and if it has 'Result' and 'Message' attributes
    if result and hasattr(result, 'Result') and hasattr(result, 'Message'):
        if result.Result == 'Success':
            return {"status": "success", "message": result.Message}
        else:
            return {"status": "error", "message": result.Message}
    else:
        return {"status": "error", "message": "An error occurred"}
    

def buy_skin(user_id, skin_id, rp_price):
    db = get_db()
    cursor = db.cursor()
    result = cursor.execute("""
        DECLARE @Result NVARCHAR(255);
        EXEC BuySkin ?, ?, ?, @Result OUTPUT;
        SELECT @Result AS Result
    """, user_id, skin_id, rp_price).fetchone()

    if result:
        return {"status": "success", "message": result.Result}
    else:
        return {"status": "error", "message": "An error occurred"}


def get_user_balance(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM GetUserBalance(?)", user_id)
    balance = cursor.fetchone()
    return balance








