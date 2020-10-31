from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField, TimeField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class formTurno(FlaskForm):

    class Meta:
        csrf = False

    hora_inicio = TimeField("Hora de Inicio",validators=[DataRequired()])
    hora_fin = TimeField("Hora de Fin",validators=[DataRequired()])
    fecha = DateField("Fecha de Turno",validators=[DataRequired()])
    telefono_visitante = StringField("Telefono del visitante",validators=[DataRequired(), Length(max=20)])
    email_visitante = EmailField("Email del visitante",validators=[DataRequired(), Email(), Length(max=255)])

