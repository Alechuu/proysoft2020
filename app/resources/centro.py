from flask import redirect, render_template, request, url_for, session, abort

from app.db import connection
from app.models.user import User
from app.models.configuracion import Configuracion
from app.models.centro import Centro
from app.models.turno import Turno
from app.helpers.auth import authenticated
from app.helpers.autorizacion import get_permisos
import requests


def index():
    if not authenticated(session):
        abort(401)
    miConfiguracion = Configuracion.get_first() 
    permisos = get_permisos(User.find_by_username(session.get("user")))
    if "centro_index" in permisos:
        centros = Centro.get_all()
        turnos = Turno.get_all()
        return render_template("centro/centros.html",permisos=permisos, conf=miConfiguracion, centros=centros)
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



def create():
    if not authenticated(session):
        abort(401)

    miConfiguracion = Configuracion.get_first()  
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    if "centro_new" in permisos:
        active_page="centro_new"
        
        try:
            Centro.create(request.form)
            notificacion="¡Se registró exitosamente el Centro "+request.form.get('nombre')+"! Puede visualizarlo en el listado."
            return render_template("centro/centro_new.html", permisos=permisos,conf=miConfiguracion, active_page=active_page,notificacion=notificacion)
        except Exception as e:
            if "for key 'email'" in str(e):
                notificacion="Ya existe un Centro con el email: "+request.form.get('email')+". Por favor, elija otro."
                return render_template("centro/centro_new.html", permisos=permisos,notificacion=notificacion, conf=miConfiguracion, active_page=active_page,centro_data=request.form)
            if "for key 'username'" in str(e):
                notificacion="Ya existe un Centro con el nombre: "+request.form.get('nombre')+". Por favor, elija otro."
                return render_template("centro/centro_new.html", permisos=permisos,notificacion=notificacion, conf=miConfiguracion, active_page=active_page,centro_data=request.form)
     