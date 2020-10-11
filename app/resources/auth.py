from flask import redirect, render_template, request, url_for, abort, session, flash
from app.db import connection
from app.models.user import User


def login():
    return render_template("auth/login.html")


def authenticate():
    ##conn = connection()
    params = request.form

    user = User.find_by_username_and_pass(params["username"], params["password"])

    if not user:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for("auth_login"))

    session["user"] = user.username
    session["first_name"] = user.first_name
    flash("La sesión se inició correctamente.")

    return redirect(url_for("dashboard"))


def logout():
    del session["user"]
    session.clear()
    flash("La sesión se cerró correctamente.")

    return redirect(url_for("index"))
