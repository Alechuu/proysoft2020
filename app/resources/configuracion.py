from flask import render_template, session, abort, redirect, url_for

from app.models.configuracion import Configuracion
from app.models.user import User
from app.helpers.auth import authenticated
from app.helpers.autorizacion import get_permisos
from app.forms.configuracion.formConfiguracion import FormConfiguracion

def index():
    if not authenticated(session):
        abort(401)

    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    if "configuracion_index" in permisos:        
        form = FormConfiguracion()
        miConfiguracion = Configuracion.get_first()  
        form.sitioHabilitado.data = miConfiguracion.habilitado  
        return render_template("configuracion.html", conf=miConfiguracion, form=form, permisos=permisos)
    else:
        # Informar error
        abort(401)


def save():
    if not authenticated(session):
        abort(401)
    active_page="configuracion"
    miConfiguracion = Configuracion.get_first()
    form = FormConfiguracion()
    if form.validate_on_submit():
        titulo = form.titulo.data
        descripcion = form.descripcion.data
        mailContacto = form.mailContacto.data
        paginado = form.paginado.data
        sitioHabilitado = form.sitioHabilitado.data
        # actualizo la configuracion                

        if miConfiguracion.titulo != titulo:
            miConfiguracion.set_titulo(titulo)
        if miConfiguracion.descripcion != descripcion:
            miConfiguracion.set_descripcion(descripcion) 
        if miConfiguracion.email != mailContacto:
            miConfiguracion.set_email(mailContacto)
        if miConfiguracion.paginado != paginado:
            miConfiguracion.set_paginado(paginado)
        if miConfiguracion.habilitado != sitioHabilitado:
            miConfiguracion.set_habilitado(sitioHabilitado)
        
        miConfiguracion.save()
        permisos = get_permisos(User.find_by_username(session.get("user")))
        notificacion = "¡Se editó correctamente la configuración del sitio!"
        return render_template("configuracion.html", conf=miConfiguracion, form=form, active_page=active_page,permisos=permisos,notificacion=notificacion)
    
    return render_template("configuracion.html", conf=miConfiguracion, form=form, active_page=active_page)