from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from . import db
from .models import Bar, Categoria, Pintxo, Usuario, Voto, Rol
from .forms import VotoForm
from .services import registrar_voto_servicio

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    form = VotoForm()

    bares_db = Bar.query.order_by(Bar.nombre_bar).all()
    categorias_db = Categoria.query.order_by(Categoria.nombre_categoria).all()

    form.categoria_id.choices = [("", "-- Elige una categoría --")] + \
                                [(cat.id_categoria, cat.nombre_categoria) for cat in categorias_db]
    form.bar_id.choices = [("", "-- Elige un bar --")] + \
                          [(bar.id_bar, bar.nombre_bar) for bar in bares_db]

    # --- Definición del diccionario de logos ---
    # IMPORTANTE: Las claves (nombres de los bares) deben coincidir
    # exactamente con los valores de 'bar.nombre_bar' de tu base de datos.
    # Las rutas son relativas a la carpeta 'static'.
    logos_dict = {
        "Bar Fermín": "images/bares/Bar_fermin_logo.png",
        "Gure Toki": "images/bares/Gure-Toki-logo.jpg",
        "Bar Charly": "images/bares/charly.jpeg",
        "La Olla": "images/bares/laolla.png",
        "Sorginzulo": "images/bares/sorginzulo.jpg",
        "Txiriboga": "images/bares/txiriboga.png",
        "Bar Urdiña": "images/bares/urdiña.png",
        "Restaurante Víctor Montes": "images/bares/victor.png",
        "Zaharra - Plaza Nueva": "images/bares/zaharra.jpg"
        # Asegúrate de que estos nombres coincidan EXACTAMENTE con los de tu base de datos
    }

    # --- Definición del diccionario de imágenes para el popup ---
    # Similar a logos_dict, las claves deben coincidir con bar.nombre_bar
    # y las rutas son relativas a 'static'
    imagenes_popup_dict = {
        "Bar Fermín": "images/collage/7.png", # Asumiendo que 7.png es para Bar Fermin
        "Gure Toki": "images/collage/4.png",  # Asumiendo que 4.png es para Gure Toki
        "Bar Charly": "images/collage/1.png",
        "La Olla": "images/collage/6.png",
        "Sorginzulo": "images/collage/5.png",
        "Txiriboga": "images/collage/3.png",
        "Bar Urdiña": "images/collage/8.png",
        "Restaurante Víctor Montes": "images/collage/2.png",
        "Zaharra - Plaza Nueva": "images/collage/9.png"
        # Añade aquí el mapeo para todos tus bares si es necesario
        # "Nombre exacto del Bar desde BD": "images/collage/nombre_archivo_imagen.ext",
    }

    return render_template('index.html',
                           bares=bares_db,
                           categorias=categorias_db,
                           form=form,
                           logos=logos_dict,  # Pasas el diccionario de logos
                           imagenes_popup=imagenes_popup_dict) # ¡NUEVO! Pasa el diccionario de imágenes para popup

# ... (El resto de tus rutas como procesar_voto_ruta y ver_votos permanecen igual) ...

@main_bp.route('/votar', methods=['POST'])
def procesar_voto_ruta():
    form = VotoForm()
    # Es buena práctica recargar las choices aquí también por si la BD cambia,
    # o si el formulario se re-renderiza con errores sin redirigir.
    form.categoria_id.choices = [("", "-- Elige una categoría --")] + \
                                [(cat.id_categoria, cat.nombre_categoria) for cat in Categoria.query.order_by(Categoria.nombre_categoria).all()]
    form.bar_id.choices = [("", "-- Elige un bar --")] + \
                          [(bar.id_bar, bar.nombre_bar) for bar in Bar.query.order_by(Bar.nombre_bar).all()]

    if form.validate_on_submit():
        nombre_votante = form.nombre_votante.data
        email_votante = form.email_votante.data
        id_categoria_seleccionada = form.categoria_id.data
        id_bar_seleccionado = form.bar_id.data

        exito, mensaje = registrar_voto_servicio(nombre_votante,
                                                email_votante,
                                                id_categoria_seleccionada,
                                                id_bar_seleccionado)

        if exito:
            flash(mensaje, 'success')
        else:
            flash(mensaje, 'danger')
        return redirect(url_for('main.index') + '#votar')
    else:
        # Si hay errores de validación, muestra los mensajes
        for field_name, error_messages in form.errors.items():
            field_label = getattr(form, field_name).label.text if hasattr(getattr(form, field_name), 'label') else field_name.capitalize()
            for error in error_messages:
                flash(f"Error en el campo '{field_label}': {error}", 'danger')

        # Si no hay errores específicos de campo pero la validación falla (raro, pero puede pasar con validadores a nivel de formulario)
        if not form.errors:
             flash('Error: Por favor, completa todos los campos del formulario correctamente.', 'danger')
        
        # Redirige de vuelta a la sección de votar para mostrar los errores.
        # Si quisieras re-renderizar la plantilla directamente aquí en lugar de redirigir,
        # necesitarías volver a cargar bares_db, categorias_db, logos_dict, e imagenes_popup_dict
        # como en la función index().
        return redirect(url_for('main.index') + '#votar')


@main_bp.route('/ver-votos')
def ver_votos():
    # Esta ruta es solo para depuración. ¡No la uses en producción sin protegerla!
    votos_en_db = Voto.query.order_by(Voto.fecha_voto.desc()).all()
    respuesta_html = "<h1>Votos Registrados (Desde Base de Datos)</h1>"
    if votos_en_db:
        respuesta_html += "<pre>"
        for voto in votos_en_db:
            votante_nombre = "N/A"
            votante_email = "N/A"
            if voto.usuario_obj:
                votante_nombre = voto.usuario_obj.nombre_usuario
                votante_email = voto.usuario_obj.email_usuario

            pintxo_nombre = "N/A"
            bar_nombre = "N/A"
            cat_nombre = "N/A"
            if voto.pintxo_obj:
                pintxo_nombre = voto.pintxo_obj.nombre_pintxo
                if voto.pintxo_obj.bar_obj:
                    bar_nombre = voto.pintxo_obj.bar_obj.nombre_bar
                if voto.pintxo_obj.categoria_obj:
                    cat_nombre = voto.pintxo_obj.categoria_obj.nombre_categoria

            respuesta_html += (f"Voto ID: {voto.id_voto}, "
                               f"Votante: {votante_nombre} ({votante_email}), "
                               f"Pintxo Votado: {pintxo_nombre} (Bar: {bar_nombre} - Cat: {cat_nombre}), "
                               f"Fecha: {voto.fecha_voto.strftime('%Y-%m-%d %H:%M:%S') if voto.fecha_voto else 'N/A'}\n")
        respuesta_html += "</pre>"
    else:
        respuesta_html += "<p>No hay votos registrados en la base de datos.</p>"
    return respuesta_html
