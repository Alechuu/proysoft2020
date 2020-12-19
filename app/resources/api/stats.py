import json
from flask import Response, request
from flask_restful import Resource
from app.models.centro import Centro
from app.models.turno import Turno


class EstadisticasTurnos(Resource):

    def get(self):
        centros = Centro.get_all_turnos_stats()
        parsed_data = []
        for centro in centros:
            parsed_data.append({
                'centro': centro.nombre,
                'turnos': len(centro.turnos)
            })
        data = {
            'count': len(centros),
            'entries': parsed_data
        }
        return Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
            )



class EstadisticasHorarios(Resource):
    def get(self):
        turnos = Turno.get_horarios_pedidos()
        parsed_data = []
        for turno in turnos:
            parsed_data.append({
                'horario': str(turno.hora_inicio)[:-3],
                'turnos': turno[1]
            })
        data = {
            'count': len(turnos),
            'entries' : parsed_data
        }
        #breakpoint()
        return Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
            )


class EstadisticasCentros(Resource):

    def get(self):
        municipio = request.args.get("municipio")
        estadistica = Centro.get_estadistica_por_municipio(municipio)
        """ estadistica = []
        estadistica.append({ 'cost': 1523, 'date': '01/01', 'profit': 1523, 'growthRate': 0.12, 'people': 100 })
        estadistica.append({ 'cost': 1223, 'date': '01/02', 'profit': 1523, 'growthRate': 0.345, 'people': 100 })
        estadistica.append({ 'cost': 2123, 'date': '01/03', 'profit': 1523, 'growthRate': 0.7, 'people': 100 })
        estadistica.append({ 'cost': 4123, 'date': '01/04', 'profit': 1523, 'growthRate': 0.31, 'people': 100 })
        estadistica.append({ 'cost': 3123, 'date': '01/05', 'profit': 1523, 'growthRate': 0.12, 'people': 100 })
        estadistica.append({ 'cost': 7123, 'date': '01/06', 'profit': 1523, 'growthRate': 0.65, 'people': 100 }) """
        data = {'lista':estadistica}
        return Response(
            json.dumps(data),
            status=200,
            mimetype='application/json'
            )
            
