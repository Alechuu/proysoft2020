import json, os, random
from datetime import datetime, timedelta

from flask import Response, request, session, current_app
from flask_restful import Resource

from app.models.turno import Turno
from app.models.centro import Centro
from app.helpers.serialize import serializeSQLAlchemy

class Turnos(Resource):

    def get(self):
        fecha = request.args.get("fecha")
        email = request.args.get("email")
        if (fecha == None or email == None):
            datos = {
                'status':400,
                'body': 'Bad Request'
            }
            return Response(
                json.dumps(datos),
                status=400,
                mimetype='application/json'
                )
        try:
            turnos = Turno.get_by_date_and_email(fecha,email)
            if turnos == []:
                datos = {
                    'status':404,
                    'body': 'Not Found',
                    'details': 'No se encontraron turnos con esos parámetros'
                }
                return Response(
                    json.dumps(datos),
                    status=404,
                    mimetype='application/json'
                    )
            parsed_data = []
            campos_no_deseados = ['id','id_centro_ayuda']
            campos_no_deseados_c = [
                'tipo_centro',
                'hora_apertura',
                'hora_cierre',
                'sitio_web',
                'email',
                'latitud',
                'longitud',
                'estado',
                'solicitud'
                ]
            for turno in turnos:
                centro = Centro.get_by_id(turno.id_centro_ayuda)
                parsed_data.append(
                    {
                        'turno':{
                            'datos':serializeSQLAlchemy(turno,campos_no_deseados),
                            'centro':serializeSQLAlchemy(centro,campos_no_deseados_c)
                        }
                    }
                    )
            datos = {
                'status': 200,
                'body': parsed_data
            }
            return Response(
                json.dumps(datos),
                status=200,
                mimetype='application/json'
                )            
        except:
            datos = {
                'status': 500,
                'body': 'Internal Server Error'
            }
            return Response(
                json.dumps(datos),
                status=500,
                mimetype='application/json'
                )  
