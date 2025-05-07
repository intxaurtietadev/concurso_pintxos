# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class VotoForm(FlaskForm):
    nombre_votante = StringField('Tu Nombre:', validators=[DataRequired(), Length(min=2, max=100)])
    email_votante = StringField('Tu Email:', validators=[DataRequired(), Email()])
    # Las opciones (choices) para SelectField se suelen popular dinámicamente en la ruta
    categoria_pintxo = SelectField('Categoría del Pintxo:', validators=[DataRequired()], coerce=str) # Usa coerce=int si los values son IDs numéricos
    bar_votado = SelectField('Selecciona el bar:', validators=[DataRequired()], coerce=str) # Usa coerce=int si los values son IDs numéricos
    submit = SubmitField('Enviar Voto')