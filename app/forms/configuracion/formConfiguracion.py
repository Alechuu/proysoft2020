from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class FormConfiguracion(FlaskForm):

    titulo = StringField("Título (requerido)", validators=[DataRequired(), Length(max=255)])
    descripcion = StringField("Descripción", validators=[Length(max=255)])
    mailContacto = EmailField("Mail de Contacto", validators=[Email()])
    paginado = IntegerField("Paginado", validators=[NumberRange(min=1, max=50)])
    sitioHabilitado = BooleanField("Sitio Habilitado")
    submit = SubmitField("Guardar")