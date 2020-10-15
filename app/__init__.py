from os import path, environ
from flask import Flask, render_template, g
from flask_session import Session
from config import config
from app.db import db
from app.resources import issue, user, auth, configuracion, centro
from app.resources.api import issue as api_issue
from app.helpers import handler
from app.helpers import auth as helper_auth
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

def create_app(environment="development"):
    # Configuración inicial de la app
    app = Flask(__name__)

    bootstrap = Bootstrap(app)

    # Carga de la configuración
    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])

    # Server Side session
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app) 

    # Configure db    
    db.init_app(app)

    # Funciones que se exportan al contexto de Jinja2
    app.jinja_env.globals.update(is_authenticated=helper_auth.authenticated)

    # Autenticación
    app.add_url_rule("/iniciar_sesion", "auth_login", auth.login)
    app.add_url_rule("/cerrar_sesion", "auth_logout", auth.logout)
    app.add_url_rule(
        "/autenticacion", "auth_authenticate", auth.authenticate, methods=["POST"]
    )

    # Rutas de Consultas
    app.add_url_rule("/consultas", "issue_index", issue.index)
    app.add_url_rule("/consultas", "issue_create", issue.create, methods=["POST"])
    app.add_url_rule("/consultas/nueva", "issue_new", issue.new)

    # Rutas de Usuarios
    #p1 = User(0,"user", "email", "password", 1, "first_name", "last_name", "roles")
    
    app.add_url_rule("/usuarios", "user_create", user.create, methods=["POST"])
    app.add_url_rule("/usuarios/nuevo", "user_new", user.new)
    app.add_url_rule("/usuarios/listar", "user_index", user.listarUsuarios)
    app.add_url_rule("/usuarios/borrar", "user_borrar", user.delete)
    app.add_url_rule("/usuarios/update", "user_update", user.update, methods=["POST"])
    app.add_url_rule("/usuarios/cambiarEstado", "user_cambiar_estado", user.cambiarEstado)


    #Rutas de Centros
    app.add_url_rule("/centros", "centro_index", centro.index)
    app.add_url_rule("/centros/crear", "centro_new", centro.new)

    #Rutas de Configuracion
    app.add_url_rule('/configuracion', "configuracion", configuracion.index)
    app.add_url_rule('/configuracion', "configuracion_save", configuracion.save, methods=["POST"])

    # Rutas de API-rest
    app.add_url_rule("/api/consultas", "api_issue_index", api_issue.index)

    # Handlers
    app.register_error_handler(404, handler.not_found_error)
    app.register_error_handler(401, handler.unauthorized_error)
    # Implementar lo mismo para el error 500 y 401

    # Ruta para el Home (usando decorator)
    app.add_url_rule("/", "home", configuracion.home)
    app.add_url_rule("/index", "home", configuracion.home)
    #@app.route("/")
    #def home():
    #    return render_template("index.html")

    
    #@app.route('/index')
    #def index():
    #    return render_template('index.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/profile')
    def profile():
        return render_template('profile.html')

    @app.route('/centros')
    def centros():
        return render_template('centros.html')

    @app.route('/usuarios')
    def usuarios():
        return render_template('usuarios.html')

   #@app.route('/new_centro')
   # def new_centro():
   #     return render_template('new_centro.html')

    # Retornar la instancia de app configurada
    return app
