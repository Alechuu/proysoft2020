from flask import redirect, render_template, request, url_for, session, abort

from app.db import connection
from app.models.user import User
from app.helpers.auth import authenticated
from app.helpers.autorizacion import get_permisos

# Protected resources
def index():
    if not authenticated(session):
        abort(401)

    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    return render_template("dashboard.html", permisos=permisos)
