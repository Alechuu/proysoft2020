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
    URL= 'https://api-referencias.proyecto2020.linti.unlp.edu.ar/municipios?page=1&per_page=135'

     
    # sending get request and saving the response as response object 
    r = requests.get(url = URL) 
    data = r.json()
    municipios = []
    for municipio in data['data']['Town']:
        municipios.append(data['data']['Town'][municipio]['name'])
       
    if "centro_new" in permisos:
        return render_template("centro/new_centro.html",permisos=permisos, conf=miConfiguracion, municipios = municipios) #centros=centros
    else:
        abort(401)


def cambiarEstado():
    if not authenticated(session):
        abort(401)
    miConfiguracion = Configuracion.get_first() 
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    if "centro_update" in permisos:
        usuarios=User.all()
        Centro.cambiarEstado(request.form.get("id_centro"))
        centros = Centro.get_all()
        notificacion = "¡Se actualizó con éxito el estado del Centro "+request.form.get("nombre")+"!"
        return render_template("centro/centros.html",usuarios=usuarios, permisos=permisos, notificacion=notificacion, conf=miConfiguracion, centros=centros)
    else:
        abort(401)

def update():
    if not authenticated(session):
        abort(401)
    miConfiguracion = Configuracion.get_first() 
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    if "centro_update" in permisos:
        usuarios=User.all()
        Centro.update(request.form)
        centros = Centro.get_all()
        notificacion = "¡Se actualizó con éxito la información del Centro "
        return render_template("centro/centros.html",usuarios=usuarios, permisos=permisos, notificacion=notificacion, conf=miConfiguracion, centros=centros)
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
        if(request.form.get('nombre') == 'error'):
            notificacion="¡Prueba de Error!"
            return render_template("centro/centro_new.html", permisos=permisos,conf=miConfiguracion, active_page=active_page,notificacion=notificacion)
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
    
   
def delete():
    if not authenticated(session):
        abort(401)
    miConfiguracion = Configuracion.get_first()  
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    if "centro_destroy" in permisos:
        usuarios = User.all()
        Centro.delete(request.form.get("id_centro"))
        centros = Centro.get_all()
        notificacion = "¡Se eliminó con éxito al Centro "+request.form.get('nombre')+"!"
        return render_template("centro/centros.html",usuarios=usuarios, permisos=permisos, notificacion=notificacion, conf=miConfiguracion, centros=centros)
    else:
        abort(401)