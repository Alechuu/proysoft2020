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

    session["user"] = user.username
    session["first_name"] = user.first_name
    flash("La sesión se inició correctamente.")

    """ usuario = User.find_by_username(session.get("user")) """
    permisos = get_permisos(user)

    return render_template("dashboard.html", permisos=permisos, conf=miConfiguracion)


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("index"))
