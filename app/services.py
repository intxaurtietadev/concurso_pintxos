from . import db
from .models import Usuario, Bar, Categoria, Pintxo, Voto, Rol # Modelos actualizados
from flask import current_app # Para logging de errores
# import datetime # No se usa directamente datetime aquí si fecha_voto usa server_default
# from datetime import timezone # No se usa directamente timezone aquí
from sqlalchemy.exc import IntegrityError # Para capturar errores de unicidad

def registrar_voto_servicio(nombre_votante, email_votante, id_categoria_seleccionada, id_bar_seleccionado):
    """
    Procesa y registra un voto. El usuario selecciona una categoría y un bar.
    El sistema busca el pintxo correspondiente a esa combinación de bar y categoría.
    Asegura que un usuario vote solo una vez POR CATEGORÍA.
    """
    try:
        # Paso 1: Buscar o crear el usuario
        usuario = Usuario.query.filter_by(email_usuario=email_votante).first()
        if not usuario:
            rol_votante = Rol.query.filter_by(rol='Lector').first()
            if not rol_votante:
                current_app.logger.error("Rol por defecto 'Lector' no encontrado en la base de datos.")
                return False, "Error de configuración del sistema: Rol de votante no encontrado."

            usuario = Usuario(
                nombre_usuario=nombre_votante,
                email_usuario=email_votante,
                pass_usuario="NOT_SET_ANONYMOUS_VOTE", # Placeholder
                estado_usuario='activo',
                id_rol=rol_votante.id_rol
            )
            db.session.add(usuario)
            db.session.flush() # Para obtener el id_usuario si es necesario antes del commit

        # Paso 2: Encontrar el Pintxo basado en la categoría y el bar seleccionados.
        # Esta lógica asume que hay un único pintxo participante por la combinación de id_bar y id_categoria.
        pintxo_a_votar = Pintxo.query.filter_by(
            id_bar=id_bar_seleccionado,
            id_categoria=id_categoria_seleccionada # El pintxo debe pertenecer a la categoría seleccionada
        ).first()

        if not pintxo_a_votar:
            bar_obj = Bar.query.get(id_bar_seleccionado)
            categoria_obj = Categoria.query.get(id_categoria_seleccionada)
            bar_nombre = bar_obj.nombre_bar if bar_obj else "Desconocido"
            cat_nombre = categoria_obj.nombre_categoria if categoria_obj else "Desconocida"
            # Mensaje de error más específico:
            current_app.logger.warning(f"Intento de voto para combinación inexistente: BarID {id_bar_seleccionado} ({bar_nombre}), CatID {id_categoria_seleccionada} ({cat_nombre})")
            return False, f"No se encontró un pintxo participante del bar '{bar_nombre}' en la categoría '{cat_nombre}'."

        # --- LÓGICA DE VALIDACIÓN DE VOTO MODIFICADA ---
        # Paso 3: Comprobar si ya existe un voto para este usuario EN ESTA CATEGORÍA.
        # La base de datos tiene una UNIQUE KEY (id_usuario, id_categoria) en la tabla `votos`.
        voto_existente_en_categoria = Voto.query.filter_by(
            id_usuario=usuario.id_usuario,
            id_categoria=id_categoria_seleccionada # Usamos la categoría seleccionada directamente
        ).first()

        if voto_existente_en_categoria:
            categoria_obj = Categoria.query.get(id_categoria_seleccionada)
            cat_nombre = categoria_obj.nombre_categoria if categoria_obj else "Desconocida"
            # Mensaje claro al usuario
            return False, f"Ya has emitido un voto en la categoría '{cat_nombre}'. Solo se permite un voto por categoría."

        # --- CREACIÓN DEL VOTO MODIFICADA ---
        # Paso 4: Crear y guardar el nuevo voto, incluyendo id_categoria.
        # El campo 'fecha_voto' usará el server_default definido en el modelo Voto (func.now()).
        nuevo_voto = Voto(
            id_usuario=usuario.id_usuario,
            id_pintxo=pintxo_a_votar.id_pintxo,
            id_categoria=id_categoria_seleccionada # Aseguramos que se guarda la categoría del voto
        )
        db.session.add(nuevo_voto)

        # Paso 5: Hacer commit de la transacción.
        db.session.commit()

        return True, f"¡Gracias por tu voto, {nombre_votante}, para el pintxo '{pintxo_a_votar.nombre_pintxo}' en la categoría '{pintxo_a_votar.categoria_obj.nombre_categoria}'!"

    except IntegrityError as e:
        db.session.rollback()
        # Este error ahora probablemente se deba a la restricción UNIQUE (id_usuario, id_categoria)
        current_app.logger.warning(f"Error de integridad al registrar voto (posiblemente voto duplicado en categoría) para {email_votante}, CatID {id_categoria_seleccionada}: {str(e)}")
        # Podríamos intentar obtener el nombre de la categoría para un mensaje más amigable
        categoria_obj = Categoria.query.get(id_categoria_seleccionada)
        cat_nombre = categoria_obj.nombre_categoria if categoria_obj else "seleccionada"
        return False, f"Error al registrar tu voto. Es posible que ya hayas votado en la categoría '{cat_nombre}'."
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error general al registrar voto para {email_votante} (CatID: {id_categoria_seleccionada}, BarID: {id_bar_seleccionado}): {str(e)}")
        return False, "Ocurrió un error inesperado al procesar tu voto. Por favor, inténtalo de nuevo más tarde."

