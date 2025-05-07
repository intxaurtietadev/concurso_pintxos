# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from . import db # Importa la instancia db desde __init__.py
from .models import Bar, CategoriaPintxo, Voto, Votante # Importa tus modelos
from .forms import VotoForm # Importa tu formulario
from .services import registrar_voto_servicio # Importa la función del servicio

main_bp = Blueprint('main', __name__) # 'main' es el nombre del blueprint

@main_bp.route('/')
def index():
    form = VotoForm() # Crea una instancia del formulario
    bares_db = Bar.query.order_by(Bar.nombre).all()
    categorias_db = CategoriaPintxo.query.order_by(CategoriaPintxo.nombre_visible).all()

    # Poblar las opciones de los SelectFields del formulario
    # Usamos (value, label). Para 'value' usamos el slug de categoría y el nombre del bar
    # ya que así lo tenías en tu HTML original y el servicio está preparado para ello.
    # Sería más robusto usar IDs si los bares pueden tener nombres duplicados (aunque en el modelo es unique).
    form.categoria_pintxo.choices = [("", "-- Elige una categoría --")] + [(cat.slug, cat.nombre_visible) for cat in categorias_db]
    form.bar_votado.choices = [("", "-- Elige un bar --")] + [(bar.nombre, bar.nombre) for bar in bares_db]

    return render_template('index.html',
                           bares=bares_db,
                           categorias=categorias_db,
                           form=form) # Pasa el formulario a la plantilla

@main_bp.route('/votar', methods=['POST'])
def procesar_voto_ruta(): # Renombrada para evitar conflicto de nombres si importas la función de servicio
    form = VotoForm() # Crea una instancia para procesar los datos
    # Es necesario repopular las opciones si vas a re-renderizar la plantilla con errores de formulario
    # (aunque aquí siempre redirigimos)
    bares_db = Bar.query.order_by(Bar.nombre).all()
    categorias_db = CategoriaPintxo.query.order_by(CategoriaPintxo.nombre_visible).all()
    form.categoria_pintxo.choices = [("", "-- Elige una categoría --")] + [(cat.slug, cat.nombre_visible) for cat in categorias_db]
    form.bar_votado.choices = [("", "-- Elige un bar --")] + [(bar.nombre, bar.nombre) for bar in bares_db]

    if form.validate_on_submit(): # Valida el formulario (incluye CSRF si Flask-WTF está bien configurado)
        nombre_votante = form.nombre_votante.data
        email_votante = form.email_votante.data
        categoria_slug = form.categoria_pintxo.data
        bar_nombre = form.bar_votado.data

        exito, mensaje = registrar_voto_servicio(nombre_votante, email_votante, categoria_slug, bar_nombre)

        if exito:
            flash(mensaje, 'success')
        else:
            flash(mensaje, 'danger')
    else:
        # Si la validación falla, Flask-WTF añade errores al objeto form.
        # Estos se pueden mostrar en la plantilla.
        # Aquí estamos redirigiendo, así que los errores del formulario no se verán directamente
        # a menos que cambies la lógica para re-renderizar index.html con el form y sus errores.
        # Por ahora, un mensaje genérico si la validación WTForms falla.
        for field, errors in form.errors.items():
             for error in errors:
                 flash(f"Error en el campo '{getattr(form, field).label.text}': {error}", 'danger')
        if not form.errors: # Si no hay errores específicos de WTForms pero validate_on_submit es False
             flash('Error: Por favor, completa todos los campos del formulario correctamente.', 'danger')


    return redirect(url_for('main.index') + '#votar') # 'main.index' porque 'index' está en el blueprint 'main'

@main_bp.route('/ver-votos')
def ver_votos():
    # ¡NO USAR EN PRODUCCIÓN SIN AUTENTICACIÓN/PROTECCIÓN!
    # Esta ruta es solo para depuración.
    votos_en_db = Voto.query.order_by(Voto.fecha_voto.desc()).all()
    respuesta_html = "<h1>Votos Registrados (Desde Base de Datos)</h1>"
    if votos_en_db:
        respuesta_html += "<pre>"
        for voto in votos_en_db:
            votante_nombre = voto.votante_obj.nombre if voto.votante_obj else "N/A"
            bar_nombre = voto.bar_votado_obj.nombre if voto.bar_votado_obj else "N/A"
            cat_nombre = voto.categoria_votada_obj.nombre_visible if voto.categoria_votada_obj else "N/A"
            respuesta_html += (f"Voto ID: {voto.id}, "
                               f"Votante: {votante_nombre} ({voto.votante_obj.email if voto.votante_obj else 'N/A'}), "
                               f"Bar: {bar_nombre}, "
                               f"Categoría: {cat_nombre}, "
                               f"Fecha: {voto.fecha_voto.strftime('%Y-%m-%d %H:%M:%S')}\n")
        respuesta_html += "</pre>"
    else:
        respuesta_html += "<p>No hay votos registrados en la base de datos.</p>"
    return respuesta_html