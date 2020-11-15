from flask import render_template, session, abort, request, jsonify
from app.helpers.auth import authenticated
from app.helpers.autorizacion import get_permisos
from app.models.configuracion import Configuracion
from app.models.centro import Centro
from app.models.user import User
from app.models.turno import Turno
from datetime import datetime

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
    start = request.args.get('fecha_ini_calendario','')#el formato es YYYY-MM-DD
    end = request.args.get('fecha_fin_calendario','')#el formato es YYYY-MM-DD
    fecha_inicio = datetime.strptime(start, '%Y-%m-%d')
    fecha_fin = datetime.strptime(end, '%Y-%m-%d')
    turnos = Turno.get_by_id_centro(id_centro, fecha_inicio, fecha_fin)
    json_list=[unTurno.serializar for unTurno in turnos]
    return jsonify(json_list)

def delete():
    id_turno = int(request.form['id_turno'], 10)
    try:
        Turno.borrar_turno(id_turno)
        mensaje = "Turno borrado."
        return jsonify(mensaje)
    except Exception as e:
        return jsonify(e)

def listarTurnos():
    if not authenticated(session):
        abort(401)
    miConfiguracion = Configuracion.get_first() 
    usuario = User.find_by_username(session.get("user"))
    permisos = get_permisos(usuario)
    active_page = "turnos_index"
    if "turnos_index" in permisos: 
        turnos = Turno.get_all()        
        return render_template("turno/list_turnos.html" ,turnos=turnos, permisos=permisos, conf=miConfiguracion, active_page=active_page)
    else:
        abort(401)
