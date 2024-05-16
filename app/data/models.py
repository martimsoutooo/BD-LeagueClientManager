from .database import get_db

def create_user(username, email, password):
    db = get_db()
    cursor = db.cursor()
    query = """
    INSERT INTO LCM.[User] (Name, Email, Password) 
    VALUES (?, ?, dbo.HashPassword(?))
    """
    cursor.execute(query, (username, email, password))
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

def verify_user(email, password):
    db = get_db()
    cursor = db.cursor()
    query = """
    SELECT * FROM LCM.[User] 
    WHERE Name = ? AND Password = dbo.HashPassword(?)
    """
    cursor.execute(query, (email, password))
    user = cursor.fetchone()
    return user is not None




