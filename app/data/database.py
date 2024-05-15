import pyodbc
from flask import g

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
        db.commit()


