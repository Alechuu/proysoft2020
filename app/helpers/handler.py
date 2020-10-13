from flask import render_template


def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "No pudimos encontrar lo que estás buscando.",
    }
    return render_template("error.html", **kwargs), 404


def unauthorized_error(e):
    kwargs = {
        "error_name": "401 Error de Autorización",
        "error_description": "No deberías estar por acá, hacé click en el botón.",
    }
    return render_template("error.html", **kwargs), 401


