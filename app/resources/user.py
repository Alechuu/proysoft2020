from flask import redirect, render_template, request, url_for, session, abort
from app.db import connection
from app.models.user import User
from app.helpers.auth import authenticated
from app.helpers.autorizacion import get_permisos

# Protected resources
def index():
    if not authenticated(session):
        abort(401)

    #conn = connection()
    users = User.all()

    return render_template("user/index.html", users=users)


def new():
    if not authenticated(session):
        abort(401)
      
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    #usuarios = User.all()
    return render_template("user/user_new.html", permisos=permisos)

    

def create():
    if not authenticated(session):
        abort(401)

    #conn = connection()
    User.create(request.form)
    return redirect(url_for("user_index"))

def delete():
    if not authenticated(session):
        abort(401)
    
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    if "usuario_index" in permisos:
        User.delete(request.args.get("id_usuario"))
        usuarios = User.all()
        notificacion = "¡Se eliminó con éxito al usuario!"
        return render_template("user/list_usuarios.html", usuarios=usuarios, permisos=permisos, notificacion=notificacion)
    else:
        abort(401)


def update():
    if not authenticated(session):
        abort(401)

    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    if "usuario_index" in permisos:
        User.update(request.form)
        usuarios = User.all()
        notificacion="¡Se actualizó con éxito al usuario: "+request.form.get("username")+"!"
        return render_template("user/list_usuarios.html", usuarios=usuarios, permisos=permisos, notificacion=notificacion)
    else:
        abort(401)

def cambiarEstado():
    if not authenticated(session):
        abort(401)

    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    if "usuario_index" in permisos:
        User.cambiarEstado(request.args.get("username"))
        usuarios = User.all()
        notificacion = "¡Se actualizó con éxito el Estado del usuario: "+request.args.get("username")+"!"
        return render_template("user/list_usuarios.html", usuarios=usuarios, permisos=permisos, notificacion=notificacion)
    else:
        abort(401)

def listarUsuarios():
    if not authenticated(session):
        abort(401)
    
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    if "usuario_index" in permisos: 
        usuarios = User.all()
        return render_template("user/list_usuarios.html", usuarios=usuarios, permisos=permisos)
    else:
        abort(401)