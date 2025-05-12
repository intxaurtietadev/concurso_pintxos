# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class VotoForm(FlaskForm):
    nombre_votante = StringField('Tu Nombre:', 
                                 validators=[DataRequired(message="Tu nombre es obligatorio."), 
                                             Length(min=2, max=100, message="El nombre debe tener entre 2 y 100 caracteres.")])
    email_votante = StringField('Tu Email:', 
                                validators=[DataRequired(message="Tu email es obligatorio."), 
                                            Email(message="Por favor, introduce un email válido.")])
    
    # Aplicar la corrección a coerce para categoria_id
    categoria_id = SelectField('Categoría del Pintxo:', 
                               validators=[DataRequired(message="Debes seleccionar una categoría.")],
                               coerce=lambda x: int(x) if x is not None and x != "" else None)

    # Aplicar la corrección a coerce para bar_id
    bar_id = SelectField('Selecciona el Bar:', 
                         validators=[DataRequired(message="Debes seleccionar un bar.")],
                         coerce=lambda x: int(x) if x is not None and x != "" else None)
    
    submit = SubmitField('Enviar Voto')
