import json, os, random
from datetime import datetime, timedelta

from flask import Response, request, session, current_app
from flask_restful import Resource

from app.models.turno import Turno
from app.models.centro import Centro
from app.helpers.serialize import serializeSQLAlchemy

class EstadisticasTurnos(Resource):

    def get(self):
        centros = Centro.get_all_turnos_stats()
        parsed_data = []
        for centro in centros:
            parsed_data.append({
                'centro':centro.nombre,
                'turnos':len(centro.turnos)
            })
        data = {
            'count':len(centros),
            'entries': parsed_data
        }
        return Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
            )