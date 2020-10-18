from flask import render_template, session, abort

from app.models.configuracion import Configuracion
from app.models.user import User
from app.helpers.autorizacion import get_permisos
from app.helpers.auth import authenticated

"""
El propósito de este controlador es simplemente levantar la configuracion del sistema y enviarla a todas las plantillas.
"""

def home():
    miConfiguracion = Configuracion.get_first()
    return render_template("index.html", conf=miConfiguracion)


def dashboard():
    if not authenticated(session):
        abort(401)
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    miConfiguracion = Configuracion.get_first()
    active_page="dashboard"
    return render_template("dashboard.html",permisos=permisos, conf=miConfiguracion, active_page=active_page)


def profile():
    if not authenticated(session):
        abort(401)
    miConfiguracion = Configuracion.get_first()
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    active_page="profile"
    return render_template("profile.html",permisos=permisos, usuario=usuario, conf=miConfiguracion, active_page=active_page)


def centros():
    miConfiguracion = Configuracion.get_first()
    active_page="centros"
    return render_template("centros.html", conf=miConfiguracion, active_page=active_page)


def usuarios():
    miConfiguracion = Configuracion.get_first()
    return render_template("usuarios.html", conf=miConfiguracion)