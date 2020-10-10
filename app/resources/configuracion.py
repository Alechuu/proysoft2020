from flask import render_template, session, abort
from app.models.configuracion import Configuracion
from app.helpers.auth import authenticated

def index():
    if not authenticated(session):
        abort(401)

    miConfiguracion = Configuracion.get_first()
    estadosSitio = {True : "Si", False: "No"}
    return render_template("configuracion.html", conf=miConfiguracion, estadosSitio=estadosSitio)


def save():
    if not authenticated(session):
        abort(401)
    