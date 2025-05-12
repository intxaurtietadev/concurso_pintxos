# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from . import db  # Importa la instancia db desde __init__.py
# Asegúrate de que estos nombres de modelos coincidan exactamente con los de tu app/models.py
from .models import Bar, Categoria, Pintxo, Usuario, Voto, Rol 
from .forms import VotoForm # Tu VotoForm adaptado para categoria_id y bar_id
from .services import registrar_voto_servicio # Tu función de servicio adaptada

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    form = VotoForm() 
    
    # Consultar datos para los desplegables y para mostrar en la página
    bares_db = Bar.query.order_by(Bar.nombre_bar).all()
    categorias_db = Categoria.query.order_by(Categoria.nombre_categoria).all()
    
    # Poblar las opciones para los SelectFields del formulario
    # El primer elemento de la tupla es el 'value' (ID), el segundo es la 'label' (texto visible)
    form.categoria_id.choices = [("", "-- Elige una categoría --")] + \
                                [(cat.id_categoria, cat.nombre_categoria) for cat in categorias_db]
    form.bar_id.choices = [("", "-- Elige un bar --")] + \
                          [(bar.id_bar, bar.nombre_bar) for bar in bares_db]

    return render_template('index.html',
                           bares=bares_db,         # Para listar bares si es necesario
                           categorias=categorias_db,  # Para listar categorías si es necesario
                           form=form)              # Pasa el objeto formulario a la plantilla

@main_bp.route('/votar', methods=['POST'])
def procesar_voto_ruta():
    form = VotoForm()  # Crea una instancia del formulario; WTForms carga los datos del POST automáticamente
    
    # Es buena práctica repoblar las 'choices' de los SelectFields
    # por si la validación falla y necesitas re-renderizar el formulario con los errores.
    # Si siempre rediriges, esto es menos crítico para la visualización de errores en la misma página del form,
    # pero no hace daño tenerlo.
    form.categoria_id.choices = [("", "-- Elige una categoría --")] + \
                                [(cat.id_categoria, cat.nombre_categoria) for cat in Categoria.query.order_by(Categoria.nombre_categoria).all()]
    form.bar_id.choices = [("", "-- Elige un bar --")] + \
                          [(bar.id_bar, bar.nombre_bar) for bar in Bar.query.order_by(Bar.nombre_bar).all()]

    if form.validate_on_submit(): # Valida el formulario (incluye CSRF si está configurado)
        nombre_votante = form.nombre_votante.data
        email_votante = form.email_votante.data
        id_categoria_seleccionada = form.categoria_id.data # Será un entero gracias a coerce=int en el form
        id_bar_seleccionado = form.bar_id.data           # Será un entero

        # Llamada al servicio con los IDs de categoría y bar
        exito, mensaje = registrar_voto_servicio(nombre_votante, 
                                                email_votante, 
                                                id_categoria_seleccionada, 
                                                id_bar_seleccionado)

        if exito:
            flash(mensaje, 'success')
        else:
            flash(mensaje, 'danger')
        # Redirigir siempre después de un POST para seguir el patrón Post/Redirect/Get
        return redirect(url_for('main.index') + '#votar') 
    else:
        # La validación del formulario falló.
        # Iterar sobre los errores y mostrarlos con flash.
        # Lo ideal sería re-renderizar la plantilla 'index.html' aquí,
        # pasando el 'form' para que los errores se muestren junto a los campos.
        for field_name, error_messages in form.errors.items():
            field_label = getattr(form, field_name).label.text if hasattr(getattr(form, field_name), 'label') else field_name.capitalize()
            for error in error_messages:
                flash(f"Error en el campo '{field_label}': {error}", 'danger')
        
        # Si se opta por redirigir, los mensajes flash son la principal retroalimentación.
        # Si no hubo errores específicos de campo pero validate_on_submit falló (raro si los validadores están bien):
        if not form.errors: 
             flash('Error: Por favor, completa todos los campos del formulario correctamente.', 'danger')
        
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