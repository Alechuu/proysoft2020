import json
from datetime import datetime, timedelta

from flask import Response, request
from flask_restful import Resource
from flask_wtf.csrf import CSRFProtect

from app.forms.api.centro import formCentros
from app.forms.api.turno import formTurno
from app.helpers.serialize import serializeSQLAlchemy
from app.models.configuracion import Configuracion
from app.models.centro import Centro
from app.models.turno import Turno



class AllCentros(Resource):
    
    def get(self):
        pagina = request.args.get('pagina')
        try:
            miConfiguracion = Configuracion.get_first()
            centros = Centro.get_all_api(int(pagina),miConfiguracion.paginado)
            if(centros[1] == []):
                datos = {'status':400,'body':'Número de página inválido','pagina_maxima':centros[2]}
                return Response(json.dumps(datos), mimetype='application/json')
            parsed_list = []
            campos_no_deseados = ['latitud','longitud','id_tipo_centro','estado','id_municipio']
            for centro in centros[1]:
                parsed_list.append(serializeSQLAlchemy(centro,campos_no_deseados))
            datos = {'status':200,'body':{'centros':parsed_list,'total':centros[0],'pagina':int(pagina)}}
            return Response(json.dumps(datos), mimetype='application/json')
        except:
            datos = {'status':500,'body':'Internal Server Error'}
            return Response(json.dumps(datos), mimetype='application/json')


class CentroID(Resource):

    def get(self,id_centro):
        try:
            centro = Centro.get_by_id(id_centro)
            campos_no_deseados = ['latitud','longitud','id_tipo_centro','estado','id_municipio']
            datos = {'status':200,'atributos':serializeSQLAlchemy(centro,campos_no_deseados)}
        except Exception as e:
            if ('__table__' in str(e)): 
                datos = {'status':401,'body':'Not Found'}
            else:
                datos = {'status':500,'body':'Internal Server Error'}
        finally:
            return Response(json.dumps(datos), mimetype='application/json')

#def api_create_new():
#    print(request.form)

class CentroNew(Resource):

    def post(self):
        form = formCentros(request.form)
        form.estado.data = False
        # Acá faltan los campos de Latitud, Longitud, id_municipio e id_tipo_centro (tipo centro se manda un id a mano pero luego no va a ser asi)
        if(not form.validate()):
            datos = {'status':400,'body':'Bad Request'}
            return Response(json.dumps(datos), mimetype='application/json')
        else:
            try:
                nuevo_centro = Centro.create(form.data)
                campos_no_deseados = ['latitud','longitud','id_tipo_centro','estado','id_municipio']
                datos = {'status':'201 Created','body':{'atributos':serializeSQLAlchemy(nuevo_centro,campos_no_deseados)}}
                return Response(json.dumps(datos), mimetype='application/json')
            except Exception as e:
                print(str(e))
                datos = {'status':500,'body':'Internal Server Error'}
                return Response(json.dumps(datos), mimetype='application/json')
            

class TurnosCentro(Resource):

    def get(self,id_centro):
        fecha = request.args.get('fecha')
        if(fecha==None):
            fecha = datetime.now().date()
        elif(Centro.get_by_id(id_centro)==None):
            datos = {'status':400,'body':'Bad Request','details':'Ese centro no existe'}
            return Response(json.dumps(datos), mimetype='application/json')
        else:
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except Exception as e:
                datos = {'status':400,'body':'Bad Request','details':'Fecha Inválida'}
                return Response(json.dumps(datos), mimetype='application/json')
        try:
            centro = Centro.get_by_id_and_date(id_centro,fecha)
            turnos_disponibles = [
                '9:00:00',
                '9:30:00',
                '10:00:00',
                '10:30:00',
                '11:00:00',
                '11:30:00',
                '12:00:00',
                '12:30:00',
                '13:00:00',
                '13:30:00',
                '14:00:00',
                '14:30:00',
                '15:00:00',
                '15:30:00',
            ]
            if(centro != None):        
                for turno in centro.turnos:
                    if(str(turno.hora_inicio) in turnos_disponibles):
                        turnos_disponibles.remove(str(turno.hora_inicio))

            turnosRespuesta = []
            for turnoLibre in turnos_disponibles:
                hora_fin = datetime.strptime(turnoLibre, '%H:%M:%S')
                hora_fin = (hora_fin + timedelta(minutes=30)).time()
                turnosRespuesta.append(
                    {
                        'centro_id':id_centro,
                        'hora_inicio':turnoLibre,
                        'hora_fin':str(hora_fin),
                        'fecha':str(fecha)

                    }
                )
            datos = {'status':200, 'turnos': turnosRespuesta }
            return Response(json.dumps(datos), mimetype='application/json')
        except Exception as e:
            datos = {'status':500,'body':'Internal Server Error'}
            return Response(json.dumps(datos), mimetype='application/json')
    

class TurnosNew(Resource):

    def post(self,id_centro):
        form = formTurno(request.form)
        if(not form.validate()):
            datos = {'status':400,'body':'Bad Request'}
            return Response(json.dumps(datos),mimetype="application/json")
        else:
            try:
                centro = Centro.get_by_id(id_centro)
                if(centro==None):
                    datos = {'status':400,'body':'Bad Request','details':'Ese centro no existe'}
                    return Response(json.dumps(datos),mimetype="application/json")
                if(Turno.get_by_hour_and_date(form.data['hora_inicio'],form.data['fecha'],id_centro)==None):  
                    turno = Turno.new(form.data)
                    Centro.agregarTurno(turno,centro)
                    datos_turno = {
                        'centro_id':id_centro,
                        'email_donante':form.data['email_visitante'],
                        'telefono_donante':form.data['telefono_visitante'],
                        'hora_inicio':str(form.data['hora_inicio']),
                        'hora_fin':str(form.data['hora_fin']),
                        'fecha':str(form.data['fecha'])
                    }
                    datos = {'status':'201 Created','body':{'atributos':datos_turno}}
                    return Response(json.dumps(datos),mimetype="application/json")
                else:
                    datos = {'status':400,'body':'Bad Request','details':'Ese turno ya esta reservado'}
                    return Response(json.dumps(datos),mimetype="application/json")                    
            except Exception as e:
                datos = {'status':500,'body':'Internal Server Error'}
                return Response(json.dumps(datos),mimetype="application/json")
