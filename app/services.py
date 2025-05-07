# app/services.py
from . import db
from .models import Votante, Bar, CategoriaPintxo, Voto
from flask import current_app # Para logging si es necesario
import datetime

def registrar_voto_servicio(nombre_votante, email_votante, categoria_slug, bar_nombre):
    """
    Procesa y registra un voto.
    Devuelve (True, mensaje_exito) o (False, mensaje_error).
    """
    try:
        votante = Votante.query.filter_by(email=email_votante).first()
        if not votante:
            votante = Votante(nombre=nombre_votante, email=email_votante)
            db.session.add(votante)
            # Puede ser útil hacer flush para obtener el ID del votante si se necesita antes del commit
            # db.session.flush()

        bar = Bar.query.filter_by(nombre=bar_nombre).first()
        categoria = CategoriaPintxo.query.filter_by(slug=categoria_slug).first()

        if not bar:
            return False, f"El bar '{bar_nombre}' no fue encontrado."
        if not categoria:
            return False, f"La categoría '{categoria_slug}' no fue encontrada."

        # Lógica de validación adicional (ej: ¿ya votó en esta categoría?)
        voto_existente = Voto.query.filter_by(votante_id=votante.id, categoria_id=categoria.id).first() # Asumiendo que votante.id ya está disponible (después de flush o commit parcial)
        if voto_existente and votante.id: # Solo si el votante ya tiene ID (ya existía o se flusheó)
            return False, "Ya has votado en esta categoría."
        
        # Si el votante es nuevo y no has hecho flush, su ID no estará disponible para la comprobación anterior
        # Una forma de manejarlo es hacer commit del votante primero, o reestructurar la lógica.
        # Por ahora, para simplificar, asumimos que la verificación se hace si el votante ya existe.

        nuevo_voto = Voto(votante_obj=votante, bar_votado_obj=bar, categoria_votada_obj=categoria, fecha_voto=datetime.datetime.utcnow())
        db.session.add(nuevo_voto)
        db.session.commit()
        return True, f"¡Gracias por tu voto, {nombre_votante}!"

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al registrar voto: {str(e)}") # Usa el logger de Flask
        return False, "Ocurrió un error al procesar tu voto. Por favor, inténtalo de nuevo."