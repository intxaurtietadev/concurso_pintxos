# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu_clave_secreta_muy_dificil_de_adivinar' # ¡CAMBIAR ESTO!
    # Asegúrate de que tu usuario y contraseña sean correctos, y que la base de datos exista
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+mysqlconnector://root:111@localhost/concurso_pintxos_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Otras configuraciones que puedas necesitar