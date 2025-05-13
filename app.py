from flask import Flask, render_template, url_for, request, redirect, flash
import datetime # Para añadir una marca de tiempo simulada

app = Flask(__name__)
# ¡IMPORTANTE! Sigue necesitando una secret_key para que flash() funcione
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # Reemplaza esto con tu propia clave secreta

# --- Simulación de "Base de Datos" en Memoria ---
bares_participantes = [
    {"id": 1, "nombre": "Bar Charly", "direccion": "Plaza Nueva, 8"},
    {"id": 2, "nombre": "Restaurante Víctor Montes", "direccion": "Plaza Nueva, 8"},
    {"id": 3, "nombre": "Txiriboga", "direccion": "Andra Maria, 13"},
    {"id": 4, "nombre": "Gure Toki", "direccion": "Plaza Nueva, 12"},
    {"id": 5, "nombre": "Sorginzulo", "direccion": "Plaza Nueva, 12"},
    {"id": 6, "nombre": "La Olla", "direccion": "Plaza Nueva, 2"},
    {"id": 7, "nombre": "Bar Fermín", "direccion": "Iturribide, 4"},
    {"id": 8, "nombre": "Bar Urdiña", "direccion": "Plaza Nueva, 5"},
    {"id": 9, "nombre": "Zaharra - Plaza Nueva", "direccion": "Barria, 4"},
]

categorias_pintxos = [
    {"id_cat": "tortilla", "nombre_visible": "Tortilla"},
    {"id_cat": "rabas", "nombre_visible": "Rabas"},
    {"id_cat": "bacalao", "nombre_visible": "Bacalao"},
    {"id_cat": "gilda", "nombre_visible": "Gilda"},
    {"id_cat": "vegano", "nombre_visible": "Vegano"},
    {"id_cat": "creativo", "nombre_visible": "Creativo / Innovador"},
]

logos_bares = {
    "Bar Charly": "images/bares/charly.jpeg",
    "Restaurante Víctor Montes": "images/bares/victor.png",
    "Txiriboga": "images/bares/txiriboga.png",
    "Gure Toki": "images/bares/Gure-Toki-logo.jpg",
    "Sorginzulo": "images/bares/sorginzulo.jpg",
    "La Olla": "images/bares/laolla.png",
    "Bar Fermín": "images/bares/Bar_fermin_logo.png",
    "Bar Urdiña": "images/bares/urdiña.png",
    "Zaharra - Plaza Nueva": "images/bares/zaharra.jpg",
}

pintxo_premios = [
    {"id": "pintxo1", "nombre_pintxo": "Mejor Pintxo Creativo/Innovador", "pintxo_image": "images/pintxos/creativo.jpg"},
    {"id": "pintxo2", "nombre_pintxo": "Mejor Pintxo de Tortilla", "pintxo_image": "images/pintxos/tortilla.jpg"},
    {"id": "pintxo3", "nombre_pintxo": "Mejor Pintxo de Bacalao", "pintxo_image": "images/pintxos/bakalao.jpeg"},
    {"id": "pintxo4", "nombre_pintxo": "Mejor Pintxo de Gilda", "pintxo_image": "images/pintxos/gilda.jpeg"},
    {"id": "pintxo5", "nombre_pintxo": "Mejor Pintxo Vegano", "pintxo_image": "images/pintxos/vegano.jpg"},
    {"id": "pintxo6", "nombre_pintxo": "Mejor Pintxo de Rabas", "pintxo_image": "images/pintxos/rabas.webp"},
]


# Lista en memoria para guardar los votos (se reinicia cada vez que reinicias el servidor)
votos_registrados = []
# --------------------------------------------

@app.route('/')
def index():
    # Pasamos las listas a la plantilla como antes
    # Podrías pasar 'votos_registrados' también si quieres mostrarlos en index.html
    return render_template('index.html',
                        bares=bares_participantes,
                        categorias=categorias_pintxos,
                        logos=logos_bares,
                        premios=pintxo_premios)
                        # votos=votos_registrados) # Descomenta si quieres mostrar votos

@app.route('/votar', methods=['POST'])
def procesar_voto():
    """
    Procesa el formulario y guarda el voto en la lista en memoria 'votos_registrados'.
    """
    # Obtener datos del formulario
    nombre_votante = request.form.get('nombre_votante')
    email_votante = request.form.get('email_votante')
    categoria_votada_id = request.form.get('categoria_pintxo')
    bar_votado_nombre = request.form.get('bar_votado')

    # Validación simple
    if nombre_votante and email_votante and categoria_votada_id and bar_votado_nombre:

        # --- SIMULACIÓN: Guardar voto en la lista en memoria ---
        nuevo_voto = {
            'id': len(votos_registrados) + 1, # ID simple basado en la longitud actual
            'nombre': nombre_votante,
            'email': email_votante,
            'categoria_id': categoria_votada_id,
            'bar_nombre': bar_votado_nombre,
            'fecha': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Marca de tiempo
        }
        votos_registrados.append(nuevo_voto)
        # ----------------------------------------------------

        # Imprimir en consola para confirmar (simulando log o BBDD)
        print("--- Voto Registrado (en memoria) ---")
        print(nuevo_voto)
        print(f"Total de votos ahora: {len(votos_registrados)}")
        # Puedes ver la lista completa si quieres: print(votos_registrados)
        print("------------------------------------")

        # Mensaje flash de éxito
        flash(f'¡Gracias por tu voto, {nombre_votante}!', 'success')

    else:
        # Mensaje flash de error si falta algún campo
        flash('Error: Por favor, completa todos los campos del formulario.', 'danger')

    # Redirige de vuelta a la sección de votación
    return redirect(url_for('index') + '#votar')

# (Opcional) Ruta para ver los votos guardados en memoria (solo para depuración)
# Accede a ella yendo a http://127.0.0.1:5000/ver-votos en tu navegador
@app.route('/ver-votos')
def ver_votos():
    # Simplemente muestra la lista de votos en formato simple
    # ¡No hagas esto en producción sin autenticación/protección!
    # Usamos <pre> para mantener el formato de la lista/diccionarios
    respuesta_html = "<h1>Votos Registrados (En Memoria)</h1><pre>"
    for voto in votos_registrados:
        respuesta_html += str(voto) + "\n" # Añade cada voto como string en una nueva línea
    respuesta_html += "</pre>"
    return respuesta_html


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')