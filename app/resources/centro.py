from flask import redirect, render_template, request, url_for, session, abort

from app.db import connection
from app.models.user import User
from app.models.configuracion import Configuracion
from app.helpers.auth import authenticated
from app.helpers.autorizacion import get_permisos


def index():
    if not authenticated(session):
        abort(401)
    miConfiguracion = Configuracion.get_first() 
    permisos = get_permisos(User.find_by_username(session.get("user")))
    if "centro_index" in permisos:
        return render_template("centro/centros.html",permisos=permisos, conf=miConfiguracion) #centros=centros
    else:
        abort(401)


def new():
    if not authenticated(session):
        abort(401)
    miConfiguracion = Configuracion.get_first() 
    permisos = get_permisos(User.find_by_username(session.get("user")))
    if "centro_new" in permisos:
        return render_template("centro/new_centro.html",permisos=permisos, conf=miConfiguracion) #centros=centros
    else:
        abort(401)