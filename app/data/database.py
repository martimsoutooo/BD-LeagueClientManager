import pyodbc
from flask import g, current_app

def get_db():
    if 'db' not in g:
        g.db = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=LeagueClientManager;Trusted_Connection=yes;')
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    app.teardown_appcontext(close_db)

    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # Criar tabela User se não existir
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='LCM.[User]' and xtype='U')
            CREATE TABLE LCM.[User] (
                ID INT PRIMARY KEY,
                Name VARCHAR(16),
                Email VARCHAR(36),
                Password VARCHAR(60),
                Rank_Points INT,
                BE INT,
                RP INT
            );
        ''')
        db.commit()


