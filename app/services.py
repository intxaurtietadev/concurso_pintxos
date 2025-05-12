# app/services.py
from . import db
from .models import Usuario, Bar, Categoria, Pintxo, Voto, Rol # Modelos actualizados
from flask import current_app # Para logging de errores
import datetime
from datetime import timezone # Para la fecha UTC correcta
from sqlalchemy.exc import IntegrityError # Para capturar errores de unicidad

def registrar_voto_servicio(nombre_votante, email_votante, id_categoria_seleccionada, id_bar_seleccionado):
    """
    Procesa y registra un voto. El usuario selecciona una categoría y un bar.
    El sistema busca el pintxo correspondiente a esa combinación.
    Asegura que un usuario vote solo una vez por ese pintxo específico.
    """
    try:
        # Paso 1: Buscar o crear el usuario
        usuario = Usuario.query.filter_by(email_usuario=email_votante).first()
        if not usuario:
            # Asignar rol por defecto (ej. 'Lector' o 'Votante')
            # Asegúrate de que este rol exista en tu tabla 'roles' con los datos iniciales.
            rol_votante = Rol.query.filter_by(rol='Lector').first() 
            if not rol_votante:
                current_app.logger.error("Rol por defecto 'Lector' no encontrado en la base de datos.")
                return False, "Error de configuración del sistema: Rol de votante no encontrado."
            
            usuario = Usuario(
                nombre_usuario=nombre_votante,
                email_usuario=email_votante,
                pass_usuario="NOT_SET_ANONYMOUS_VOTE", # Placeholder. ¡Nunca guardes contraseñas reales así!
                estado_usuario='activo', # O el estado por defecto que definas
                id_rol=rol_votante.id_rol 
            )
            db.session.add(usuario)
            # Hacemos flush para que el nuevo usuario obtenga un id_usuario si lo necesitas
            # inmediatamente para otras comprobaciones antes del commit final.
            db.session.flush() 
        
        # Paso 2: Encontrar el Pintxo basado en la categoría y el bar seleccionados.
        # Esta lógica asume que hay un único pintxo participante por la combinación de id_bar y id_categoria.
        # Si un bar puede tener múltiples pintxos en la misma categoría, esta lógica necesitaría cambiar
        # o el formulario necesitaría un paso más para seleccionar el pintxo específico.
        pintxo_a_votar = Pintxo.query.filter_by(
            id_bar=id_bar_seleccionado,
            id_categoria=id_categoria_seleccionada
        ).first()

        if not pintxo_a_votar:
            # Para un mensaje de error más amigable, obtenemos los nombres
            bar_obj = Bar.query.get(id_bar_seleccionado)
            categoria_obj = Categoria.query.get(id_categoria_seleccionada)
            bar_nombre = bar_obj.nombre_bar if bar_obj else "Desconocido"
            cat_nombre = categoria_obj.nombre_categoria if categoria_obj else "Desconocida"
            return False, f"No se encontró un pintxo participante para la categoría '{cat_nombre}' en el bar '{bar_nombre}'."

        # Paso 3: Comprobar si ya existe un voto para este usuario y este pintxo específico.
        # La base de datos tiene una UNIQUE KEY (id_usuario, id_pintxo) en la tabla `votos`
        # que también prevendría duplicados, pero esta comprobación da un mensaje más amigable.
        voto_existente = Voto.query.filter_by(id_usuario=usuario.id_usuario, id_pintxo=pintxo_a_votar.id_pintxo).first()
        if voto_existente:
            return False, f"Ya has votado por el pintxo '{pintxo_a_votar.nombre_pintxo}'."

        # Paso 4: Crear y guardar el nuevo voto.
        # El campo 'fecha_voto' usará el default definido en el modelo Voto.
        nuevo_voto = Voto(
            id_usuario=usuario.id_usuario, # Asignamos directamente los IDs
            id_pintxo=pintxo_a_votar.id_pintxo
            # Si prefieres usar los objetos y tienes los backrefs configurados:
            # usuario_obj=usuario,
            # pintxo_obj=pintxo_a_votar
        )
        db.session.add(nuevo_voto)
        
        # Paso 5: Hacer commit de la transacción para guardar los cambios en la base de datos.
        db.session.commit() 
        
        return True, f"¡Gracias por tu voto, {nombre_votante}, para el pintxo '{pintxo_a_votar.nombre_pintxo}'!"

    except IntegrityError as e: # Captura específicamente errores de violación de unicidad
        db.session.rollback() 
        # Es bueno loguear el error real para depuración
        current_app.logger.warning(f"Intento de voto duplicado (IntegrityError) para {email_votante}, pintxo ID {pintxo_a_votar.id_pintxo if 'pintxo_a_votar' in locals() and pintxo_a_votar else 'desconocido'}: {str(e)}")
        return False, "Parece que ya has votado por este pintxo (error de integridad)."
    except Exception as e: # Captura cualquier otra excepción
        db.session.rollback() 
        current_app.logger.error(f"Error general al registrar voto para {email_votante} (CatID: {id_categoria_seleccionada}, BarID: {id_bar_seleccionado}): {str(e)}")
        return False, "Ocurrió un error al procesar tu voto. Por favor, inténtalo de nuevo más tarde."
