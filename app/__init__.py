# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# Importa tu clase de configuración. Asumiendo que config.py está en el directorio raíz,
# y que el directorio raíz está en el PYTHONPATH cuando ejecutas la app.
from config import Config # Esto funciona si 'config.py' está en el mismo nivel que el script que ejecuta la app o en PYTHONPATH

db = SQLAlchemy() # Inicializa la extensión, pero sin la app todavía

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class) # Carga la configuración desde el objeto

    db.init_app(app) # Vincula SQLAlchemy con la instancia de la aplicación Flask

    # Importar y registrar Blueprints
    # Los Blueprints ayudan a organizar las rutas
    from .routes import main_bp  # Asumiendo que en routes.py creas un Blueprint llamado main_bp
    app.register_blueprint(main_bp)

    # Asegurarse de que los modelos sean conocidos por SQLAlchemy
    # Esto se puede hacer importándolos aquí o asegurándote de que se importen
    # en algún lugar después de que `db` se haya inicializado con `app`.
    # Si tus rutas importan los modelos, y las rutas se importan aquí (a través del blueprint),
    # entonces los modelos serán registrados.
    from . import models # Esto ayuda a que SQLAlchemy detecte los modelos

    return app