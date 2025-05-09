from . import db
from .models import Votante, Bar, CategoriaPintxo, Voto
from flask import current_app # Para logging de errores
import datetime

def registrar_voto_servicio(nombre_votante, email_votante, categoria_slug, bar_nombre):
    """
    Procesa y registra un voto, asegurando que un votante vote solo una vez por categoría.
    Maneja votantes nuevos obteniendo su ID con flush antes de las comprobaciones.
    Devuelve (True, mensaje_exito) o (False, mensaje_error).
    """
    try:
        # Paso 1: Buscar el votante por email.
        # verificamos si el votante existe
        votante = Votante.query.filter_by(email=email_votante).first()
        if not votante:
            # Si no existe lo creamos
            votante = Votante(nombre=nombre_votante, email=email_votante)
            db.session.add(votante)
            # Paso 2: Hacer db.session.flush() para que el nuevo votante obtenga un ID.
            db.session.flush()
            # Ahora, votante.id tiene un valor incluso si el votante es nuevo. 'votante' es un objeto (ya sea uno existente o uno nuevo después del flush)
        # y tiene un 'votante.id' válido.


        # Obtener el bar y la categoría (estos deben existir previamente en la BBDD)
        bar = Bar.query.filter_by(nombre=bar_nombre).first()
        if not bar:
            return False, f"El bar '{bar_nombre}' no fue encontrado."
        
        categoria = CategoriaPintxo.query.filter_by(slug=categoria_slug).first()
        if not categoria:
            return False, f"La categoría '{categoria_slug}' no fue encontrada."

        # Paso 3: Comprobar si ya existe un voto para este votante.id en esta categoria.id
        voto_existente = Voto.query.filter_by(votante_id=votante.id, categoria_id=categoria.id).first() # Asumiendo que votante.id ya está disponible (después de flush o commit parcial)
        if voto_existente and votante.id: 
            # Solo si el votante ya tiene ID (ya existía o se flusheó)
            return False, "Ya has votado en esta categoría."
        
        # Paso 4: Crear el nuevo objeto Voto y añadirlo a la sesión.
        # Usamos los objetos relacionados; SQLAlchemy se encargará de las claves foráneas.
        nuevo_voto = Voto(
            votante_obj=votante, bar_votado_obj=bar, categoria_votada_obj=categoria)
        db.session.add(nuevo_voto)
        db.session.commit()
        
        return True, f"¡Gracias por tu voto, {nombre_votante}!"

    except Exception as e:
        # Si ocurre cualquier error durante el proceso (ej. error de base de datos al hacer flush o commit),
        # revertimos todos los cambios pendientes en esta sesión.
        db.session.rollback()
        current_app.logger.error(f"Error al registrar voto para {email_votante} en categoría {categoria_slug} para bar {bar_nombre}: {str(e)}") # Usa el logger de Flask
        return False, "Ocurrió un error al procesar tu voto. Por favor, inténtalo de nuevo."