# app/routes.py
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
        "Bar Fermin": "images/bares/Bar_fermin_logo.png",
        "Gure Toki": "images/bares/Gure-Toki-logo.jpg",
        "Bar Charly": "images/bares/charly.jpeg", # Usando charly.jpeg; images.jpeg parecía ser el mismo
        "La Olla de la Plaza Nueva": "images/bares/laolla.png", # Asumiendo este nombre completo
        "Sorginzulo": "images/bares/sorginzulo.jpg",
        "Txiriboga": "images/bares/txiriboga.png",
        "Bar Urdiña": "images/bares/urdiña.png", # Nota: el archivo se llama urdiña.png
        "Victor Montes": "images/bares/victor.png",
        "Zaharra": "images/bares/zaharra.jpg"
        # --- Añade más bares aquí si es necesario ---
        # "Nombre exacto del Bar desde BD": "images/bares/nombre_archivo_logo.ext",
    }
    
    # Opcional: Si quieres una lógica más dinámica para construir logos_dict
    # basado en los bares_db que ya tienes, y si tus nombres de archivo siguen un patrón predecible:
    # logos_dict = {}
    # for bar_obj in bares_db:
    #     # Ejemplo de patrón: el nombre del archivo es el nombre del bar en minúsculas,
    #     # con espacios reemplazados por guiones bajos, y extensión .png
    #     # logo_filename = f"images/bares/{bar_obj.nombre_bar.lower().replace(' ', '_')}.png"
    #     # logos_dict[bar_obj.nombre_bar] = logo_filename
    #     # ESTA ES UNA IDEA AVANZADA, el diccionario manual de arriba es más simple para empezar.
    #     # El diccionario manual que he puesto arriba es más seguro si los nombres de archivo no siguen un patrón estricto.

    return render_template('index.html',
                           bares=bares_db,
                           categorias=categorias_db,
                           form=form,
                           logos=logos_dict) # Pasar el diccionario a la plantilla

# ... (El resto de tus rutas como procesar_voto_ruta y ver_votos permanecen igual) ...

# Asegúrate de que el resto de tus rutas (@main_bp.route('/votar', ...) etc. están aquí
@main_bp.route('/votar', methods=['POST'])
def procesar_voto_ruta():
    form = VotoForm()
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
        for field_name, error_messages in form.errors.items():
            field_label = getattr(form, field_name).label.text if hasattr(getattr(form, field_name), 'label') else field_name.capitalize()
            for error in error_messages:
                flash(f"Error en el campo '{field_label}': {error}", 'danger')

        if not form.errors:
             flash('Error: Por favor, completa todos los campos del formulario correctamente.', 'danger')
        
        # Para re-renderizar con errores en la misma página (alternativa a redirigir siempre):
        # Si haces esto, necesitarás volver a cargar bares_db, categorias_db y logos_dict aquí también
        # return render_template('index.html', form=form, bares=Bar.query.all(), categorias=Categoria.query.all(), logos=logos_dict_regenerado_aqui)
        
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