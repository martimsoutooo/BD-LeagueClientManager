import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_difficult_to_guess_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
