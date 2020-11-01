from flask import render_template, session, abort, request, jsonify
from app.helpers.auth import authenticated
from app.helpers.autorizacion import get_permisos
from app.models.configuracion import Configuracion
from app.models.centro import Centro
from app.models.user import User
from app.models.turno import Turno

def index():
    if not authenticated(session):
        abort(401)
    miConfiguracion = Configuracion.get_first() 
    permisos = get_permisos(User.find_by_username(session.get("user")))    
    if "centro_index" in permisos: 
        id_centro = request.form["id_centro"]       
        centro = Centro.get_by_id(id_centro)
        return render_template("turno/turno.html",permisos=permisos, conf=miConfiguracion, centro=centro)
    else:
        abort(401)

def get_turnos_by_centro():
    id_centro = request.args.get('parametro_id_centro','')
    #start = request.args.get('start','')#el formato es UNIX_TIMESTAMP, hay que convertir
    #end = request.args.get('end','')#el formato es UNIX_TIMESTAMP, hay que convertir
    #hora_inicio = datetime.fromtimestamp(start)
    #hora_fin = datetime.fromtimestamp(end)
    #fecha = datetime.fromtimestamp(start)
    turnos = Turno.get_by_id_centro(id_centro)
    json_list=[unTurno.serializar for unTurno in turnos]
    return jsonify(json_list)
