from flask import redirect, render_template, request, url_for, abort, session, flash

from app.db import connection
from app.models.user import User
from app.models.configuracion import Configuracion
from app.helpers.autorizacion import get_permisos


def login():
    miConfiguracion = Configuracion.get_first() 
    return render_template("auth/login.html", conf=miConfiguracion)


def authenticate():
    ##conn = connection()
    miConfiguracion = Configuracion.get_first() 
    params = request.form
    user = User.find_by_username_and_pass(params["username"], params["password"])
    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_login",error=True))

    permisos = get_permisos(user)
    if ("usuario_new" not in permisos) and (miConfiguracion.habilitado == 0):
        abort(401)
    else:
        if user.activo == 1:
            session["user"] = user.username
            session["first_name"] = user.first_name
            return redirect(url_for("profile"))
        else:
            abort(401)


def logout():
    del session["user"]
    del session["first_name"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("index"))
