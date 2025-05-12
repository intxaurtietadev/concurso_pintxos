from app import create_app, db # Importa la fábrica y la instancia de db
# Importa tus modelos para que estén disponibles en el contexto del shell
from app.models import Bar, CategoriaPintxo, Votante, Voto

flask_app = create_app('config.Config')

@flask_app.shell_context_processor
def make_shell_context():
    from app.models import Bar, Categoria, Pintxo, Usuario, Voto, Rol # Importa todos tus modelos actuales
    return {'db': db, 'Bar': Bar, 'Categoria': Categoria, 'Pintxo': Pintxo, 
            'Usuario': Usuario, 'Voto': Voto, 'Rol': Rol}

if __name__ == '__main__':
    # Si ejecutas con 'python app.py', asegúrate de que debug sea True para desarrollo
    flask_app.run(debug=True, host='0.0.0.0')