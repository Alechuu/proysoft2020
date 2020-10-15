from flask import render_template
from app.models.configuracion import Configuracion

"""
El propósito de este controlador es simplemente levantar la configuracion del sistema y enviarla a todas las plantillas.
"""

def home():
    miConfiguracion = Configuracion.get_first()
    return render_template("index.html", conf=miConfiguracion)

def dashboard():
    miConfiguracion = Configuracion.get_first()
    return render_template("dashboard.html", conf=miConfiguracion)

def profile():
    miConfiguracion = Configuracion.get_first()
    return render_template("profile.html", conf=miConfiguracion)

def centros():
    miConfiguracion = Configuracion.get_first()
    return render_template("centros.html", conf=miConfiguracion)

def usuarios():
    miConfiguracion = Configuracion.get_first()
    return render_template("usuarios.html", conf=miConfiguracion)

