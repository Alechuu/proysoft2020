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
    if "usuario_new" in permisos:
        return render_template("user/user_new.html", permisos=permisos)
    else:
        abort(401)


def create():
    if not authenticated(session):
        abort(401)

    #conn = connection()
    User.create(request.form)
    return redirect(url_for("user_index"))

def delete():
    if not authenticated(session):
        abort(401)
    
    User.delete(request.args.get("id_usuario"))
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    usuarios = User.all()
    return render_template("user/list_usuarios.html", usuarios=usuarios, permisos=permisos)


def update():
    if not authenticated(session):
        abort(401)
    
    User.update(request.form)
    print(request.form)
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    usuarios = User.all()
    return render_template("user/list_usuarios.html", usuarios=usuarios, permisos=permisos)



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