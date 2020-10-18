from flask import redirect, render_template, request, url_for, session, abort
from app.db import connection
from app.models.user import User
from app.models.configuracion import Configuracion
from app.helpers.auth import authenticated
from app.helpers.autorizacion import get_permisos

# Protected resources
def index():
    if not authenticated(session):
        abort(401)

    #conn = connection()
    users = User.all()
    miConfiguracion = Configuracion.get_first()
    return render_template("user/index.html", users=users, conf=miConfiguracion)


def new():
    if not authenticated(session):
        abort(401)
    miConfiguracion = Configuracion.get_first()  
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    active_page="user_new"

    
    #usuarios = User.all()
    return render_template("user/user_new.html", permisos=permisos, conf=miConfiguracion, active_page=active_page)

    

def create():
    if not authenticated(session):
        abort(401)

    #conn = connection()
    miConfiguracion = Configuracion.get_first()  
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    active_page="user_new"
    if(request.form.get('password') != request.form.get('confirm_password')):
        notificacion="¡Las contraseñas no coinciden!"
        return render_template("user/user_new.html", permisos=permisos,conf=miConfiguracion, active_page=active_page,notificacion=notificacion,user_data=request.form)
    
    try:
        User.create(request.form)
        notificacion="¡Se registró exitosamente el usuario "+request.form.get('username')+"! Puede visualizarlo en el listado."
        return render_template("user/user_new.html", permisos=permisos,conf=miConfiguracion, active_page=active_page,notificacion=notificacion)
    except Exception as e:
        if "for key 'email'" in str(e):
            notificacion="Ya existe un usuario con el email: "+request.form.get('email')+". Por favor, elija otro."
            return render_template("user/user_new.html", permisos=permisos,notificacion=notificacion, conf=miConfiguracion, active_page=active_page,user_data=request.form)
        if "for key 'username'" in str(e):
            notificacion="Ya existe un usuario con el nombre de usuario: "+request.form.get('username')+". Por favor, elija otro."
            return render_template("user/user_new.html", permisos=permisos,notificacion=notificacion, conf=miConfiguracion, active_page=active_page,user_data=request.form)
            
   
def delete():
    if not authenticated(session):
        abort(401)
    miConfiguracion = Configuracion.get_first()  
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    if "usuario_index" in permisos:
        User.delete(request.args.get("id_usuario"))
        usuarios = User.all()
        notificacion = "¡Se eliminó con éxito al usuario!"
        return render_template("user/list_usuarios.html", usuarios=usuarios, permisos=permisos, notificacion=notificacion, conf=miConfiguracion)
    else:
        abort(401)


def update():
    if not authenticated(session):
        abort(401)
    miConfiguracion = Configuracion.get_first() 
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    if "usuario_index" in permisos:
        try:
            User.update(request.form)
        except:
            usuarios = User.all()
            notificacion="¡El Email: "+request.form.get("email")+" ya existe, ingrese otro!"
            return render_template("user/list_usuarios.html", usuarios=usuarios, permisos=permisos, notificacion=notificacion)
        usuarios = User.all()
        notificacion="¡Se actualizó con éxito al usuario: "+request.form.get("username")+"!"
        return render_template("user/list_usuarios.html", usuarios=usuarios, permisos=permisos, notificacion=notificacion, conf=miConfiguracion)
    else:
        abort(401)

def cambiarEstado():
    if not authenticated(session):
        abort(401)
    miConfiguracion = Configuracion.get_first() 
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    if "usuario_index" in permisos:
        User.cambiarEstado(request.args.get("username"))
        usuarios = User.all()
        notificacion = "¡Se actualizó con éxito el Estado del usuario: "+request.args.get("username")+"!"
        return render_template("user/list_usuarios.html", usuarios=usuarios, permisos=permisos, notificacion=notificacion, conf=miConfiguracion)
    else:
        abort(401)

def listarUsuarios():
    if not authenticated(session):
        abort(401)
    miConfiguracion = Configuracion.get_first() 
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    active_page = "user_index"
    if "usuario_index" in permisos: 
        usuarios = User.all()
        return render_template("user/list_usuarios.html", usuarios=usuarios, permisos=permisos, conf=miConfiguracion, active_page=active_page )
    else:
        abort(401)