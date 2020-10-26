from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField, BooleanField, SubmitField, TimeField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class formCentros(FlaskForm):

    class Meta:
        csrf = False
    
    nombre = StringField("Nombre Centro", validators=[DataRequired(), Length(max=255)])
    direccion = StringField("Dirección Centro", validators=[DataRequired(), Length(max=255)])
    telefono = StringField("Teléfono Centro", validators=[DataRequired(), Length(max=20)])
    hora_apertura = TimeField("Hora de Apertura", validators=[DataRequired()])
    hora_cierre = TimeField("Hora de Cierre", validators=[DataRequired()])
    tipo = StringField("Tipo de Centro", validators=[DataRequired()])
    sitio_web = StringField("Sitio Web de Centro", validators=[DataRequired(), Length(max=60)])
    email = EmailField("Email de Centro", validators=[DataRequired(),Email(), Length(max=255)])
    estado = BooleanField("Centro Habilitado")

