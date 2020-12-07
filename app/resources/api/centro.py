import json, os, random
from datetime import datetime, timedelta

from flask import Response, request, session, current_app
from flask_restful import Resource
from flask_wtf.csrf import CSRFProtect

# ESTO ROMPE EL MODELO MVC. HAY QUE HACER UN METODO EN EL RECURSO USER
# IMPORTAR DIRECTAMENTE EL MODELO ROMPE EL MVC
from app.models.user import User 
# <== ------------------------------------------------------------ =>>
from app.forms.api.centro import formCentros
from app.forms.api.turno import formTurno
from app.helpers.serialize import serializeSQLAlchemy
from app.helpers.geocoder import geocoder as Geocoder
from app.models.configuracion import Configuracion
from app.models.centro import Centro
from app.models.turno import Turno
from app.helpers.autorizacion import get_permisos


class AllCentros(Resource):

    def get(self):
        pagina = request.args.get('pagina')
        if pagina == None:
            pagina = 1
        try:
            miConfiguracion = Configuracion.get_first()
            centros = Centro.get_all_api(int(pagina), miConfiguracion.paginado)
            if(centros[1] == []):
                datos = {'status': 400, 'body': 'Número de página inválido',
                         'pagina_maxima': centros[2]}
                return Response(json.dumps(datos), mimetype='application/json')
            parsed_list = []
            campos_no_deseados = ['solicitud', 'estado']
            for centro in centros[1]:
                parsed_list.append(serializeSQLAlchemy(
                    centro, campos_no_deseados))
            datos = {'status': 200, 'body': {'centros': parsed_list,
                                             'total': centros[0], 'pagina': int(pagina)}}
            return Response(json.dumps(datos), mimetype='application/json')
        except Exception as e:
            print(str(e))
            datos = {'status': 500, 'body': 'Internal Server Error'}
            return Response(json.dumps(datos), mimetype='application/json')


class CentroID(Resource):

    def get(self, id_centro):
        try:
            centro = Centro.get_by_id(id_centro)
            datos = {'status': 200, 'atributos': serializeSQLAlchemy(
                centro)}
        except Exception as e:
            if ('__table__' in str(e)):
                datos = {'status': 404, 'body': 'Not Found'}
            else:
                print(str(e))
                datos = {'status': 500, 'body': 'Internal Server Error'}
        finally:
            return Response(json.dumps(datos), mimetype='application/json')


class CentroNew(Resource):

    def post(self):
        form = formCentros(request.form)
        pdf_visita = request.files['path_pdf']
        # Apendo el path del archivo al formulario
        if(os.path.exists(current_app.root_path+"/static/uploads/" + (pdf_visita.filename).replace(" ", ""))):
            secuencia = 'abcdefghijklmnopqrst'
            result_str = ''.join((random.choice(secuencia) for i in range(30)))
            nombre_archivo = result_str+(pdf_visita.filename).replace(" ", "")
            form.path_pdf.data = "/static/uploads/" + nombre_archivo
            pdf_visita.save(current_app.root_path+"/static/uploads/" + nombre_archivo)
        else:
            form.path_pdf.data = "/static/uploads/" + (pdf_visita.filename).replace(" ", "")
            # Guardo el archivo
            pdf_visita.save(current_app.root_path+"/static/uploads/" +(pdf_visita.filename).replace(" ", ""))
        if(not form.validate()):
            datos = {'status': 400, 'body': 'Bad Request'}
            return Response(json.dumps(datos), mimetype='application/json')
        else:
            try:
                if(request.form['latitud'] == "" and request.form['longitud'] == ""):
                    coords = Geocoder(form.data['direccion'])
                else:
                    coords = [request.form['latitud'],request.form['longitud']]
                #breakpoint()
                usuario_logueado = session.get('user')
                if(usuario_logueado == None):
                    solicitud = "ESPERANDO_REVISION"
                    form.estado.data = False
                else:
                    usuario_logueado = User.find_by_username(usuario_logueado) 
                    permisos = get_permisos(usuario_logueado)
                    if 'centro_new' in permisos:
                        solicitud = "ACEPTADO"
                        form.estado.data = True
            
                nuevo_centro = Centro.create(form.data, coords, solicitud)
                campos_no_deseados = ['latitud', 'longitud']
                datos = {'status': '201 Created', 'body': {
                    'atributos': serializeSQLAlchemy(nuevo_centro, campos_no_deseados)}}
                return Response(json.dumps(datos), mimetype='application/json')
            except Exception as e:
                print(str(e))
                if('400 Bad Request' in str(e)):
                    datos = {'status': 400, 'body': 'Bad Request'}
                    return Response(json.dumps(datos), mimetype='application/json')                    
                datos = {'status': 500, 'body': 'Internal Server Error'}
                return Response(json.dumps(datos), mimetype='application/json')


class TurnosCentro(Resource):

    def get(self, id_centro):
        fecha = request.args.get('fecha')
        if(fecha == None):
            fecha = datetime.now().date()
        elif(Centro.get_by_id(id_centro) == None):
            datos = {'status': 400, 'body': 'Bad Request',
                     'details': 'Ese centro no existe'}
            return Response(json.dumps(datos), mimetype='application/json')
        else:
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except Exception as e:
                datos = {'status': 400, 'body': 'Bad Request',
                         'details': 'Fecha Inválida'}
                return Response(json.dumps(datos), mimetype='application/json')
        try:
            turnos = Turno.get_by_id_centro(id_centro, fecha, fecha)
            turnos_disponibles = [
                '09:00',
                '09:30',
                '10:00',
                '10:30',
                '11:00',
                '11:30',
                '12:00',
                '12:30',
                '13:00',
                '13:30',
                '14:00',
                '14:30',
                '15:00',
                '15:30',
            ]
            if(turnos != None):
                for turno in turnos:
                    if((turno.hora_inicio).strftime("%H:%M") in turnos_disponibles):
                        turnos_disponibles.remove((turno.hora_inicio).strftime("%H:%M"))

            turnosRespuesta = []
            for turnoLibre in turnos_disponibles:
                hora_fin = datetime.strptime(turnoLibre, '%H:%M')
                hora_fin = ((hora_fin + timedelta(minutes=30)).time()).strftime("%H:%M")
                turnosRespuesta.append(
                    {
                        'centro_id': id_centro,
                        'hora_inicio': turnoLibre,
                        'hora_fin': str(hora_fin),
                        'fecha': str(fecha)

                    }
                )
            datos = {'status': 200, 'turnos': turnosRespuesta}
            return Response(json.dumps(datos), mimetype='application/json')
        except Exception as e:
            datos = {'status': 500, 'body': 'Internal Server Error'}
            return Response(json.dumps(datos), mimetype='application/json')


class TurnosNew(Resource):

    def post(self, id_centro):
        form = formTurno(request.form)
        if(not form.validate()):
            datos = {'status': 400, 'body': 'Bad Request'}
            return Response(json.dumps(datos), mimetype="application/json")
        else:
            try:
                centro = Centro.get_by_id(id_centro)
                if(centro == None):
                    datos = {'status': 400, 'body': 'Bad Request',
                             'details': 'Ese centro no existe'}
                    return Response(json.dumps(datos), mimetype="application/json")
                # Armo fecha y hora con los argumentos del request para controlar que el turno se cree en el futuro
                # form.data['fecha'] es de clase 'datetime.date' y form.data['hora_inicio'] es de clase 'datetime.time'
                # combino ambos datos para generar un datetime
                fh_turno = datetime.combine(
                    form.data['fecha'], form.data['hora_inicio'])
                now = datetime.now()
                if(now > fh_turno):
                    datos = {'status': 400, 'body': 'Bad Request',
                             'details': 'Verifique que la fecha y/o la hora del turno sean posteriores a este momento'}
                    return Response(json.dumps(datos), mimetype="application/json")
                if(Turno.get_by_hour_and_date(form.data['hora_inicio'], form.data['fecha'], id_centro) == None):
                    turno = Turno.new(form.data)
                    Centro.agregarTurno(turno, centro)
                    datos_turno = {
                        'centro_id': id_centro,
                        'centro_nombre': centro.nombre,
                        'centro_municipio': centro.municipio,
                        'email_donante': form.data['email_visitante'],
                        'telefono_donante': form.data['telefono_visitante'],
                        'hora_inicio': str(form.data['hora_inicio']),
                        'hora_fin': str(form.data['hora_fin']),
                        'fecha': str(form.data['fecha'])
                    }
                    datos = {'status': '201 Created',
                             'body': {'atributos': datos_turno}, 'details': 'El turno se ha creado de manera exitosa.'}
                    return Response(json.dumps(datos), mimetype="application/json")
                else:
                    datos = {'status': 400, 'body': 'Bad Request',
                             'details': 'Ese turno ya esta reservado'}
                    return Response(json.dumps(datos), mimetype="application/json")
            except Exception as e:
                datos = {'status': 500, 'body': 'Internal Server Error'}
                return Response(json.dumps(datos), mimetype="application/json")


class TurnosUpdate(Resource):

    def post(self, id_centro):
        form = formTurno(request.form)
        if(not form.validate()):
            datos = {'status': 400, 'body': 'Bad Request'}
            return Response(json.dumps(datos), mimetype="application/json")
        else:
            try:
                # chequeos de existencia de centro y turno
                centro = Centro.get_by_id(id_centro)
                if(not centro):
                    datos = {'status': 400, 'body': 'Bad Request',
                             'details': 'Ese centro no existe'}
                    return Response(json.dumps(datos), mimetype="application/json")
                id_turno = int(request.form['id_turno'], 10)
                turno = Turno.get_by_id(id_turno)
                if(not turno):
                    datos = {'status': 400, 'body': 'Bad Request',
                             'details': 'El turno no existe'}
                    return Response(json.dumps(datos), mimetype="application/json")
                # Armo fecha y hora con los argumentos del request para controlar que el turno se cree en el futuro
                # form.data['fecha'] es de clase 'datetime.date' y form.data['hora_inicio'] es de clase 'datetime.time'
                # combino ambos datos para generar un datetime
                fh_turno = datetime.combine(
                    form.data['fecha'], form.data['hora_inicio'])
                now = datetime.now()
                if(now > fh_turno):
                    datos = {'status': 400, 'body': 'Bad Request',
                             'details': 'Verifique que la fecha y/o la hora del turno sean posteriores a este momento'}
                    return Response(json.dumps(datos), mimetype="application/json")
                # chequeo que el horario no esté ocupado por otro turno
                t = Turno.get_by_hour_and_date(form.data['hora_inicio'], form.data['fecha'], id_centro)
                if(not t or t.id == id_turno):
                    Turno.update(turno, form.data)
                    datos_turno = {
                        'centro_id': id_centro,
                        'id_turno': id_turno,
                        'email_donante': form.data['email_visitante'],
                        'telefono_donante': form.data['telefono_visitante'],
                        'hora_inicio': str(form.data['hora_inicio']),
                        'hora_fin': str(form.data['hora_fin']),
                        'fecha': str(form.data['fecha'])
                    }
                    datos = {'status': '200 OK', 'body': {'atributos': datos_turno},
                             'details': 'El turno se ha actualizado de manera exitosa.'}
                    return Response(json.dumps(datos), mimetype="application/json")
                else:
                    datos = {'status': 400, 'body': 'Bad Request',
                             'details': 'Ese turno ya esta reservado'}
                    return Response(json.dumps(datos), mimetype="application/json")
            except Exception as e:
                datos = {'status': 500, 'body': 'Internal Server Error'}
                return Response(json.dumps(datos), mimetype="application/json")

class TurnosCentroRangoFecha(Resource):

    def get(self):
        try:
            id_centro = request.args.get('id_centro', type=int)
            if(not id_centro):
                datos = {'status': 400, 'body': 'Bad Request',
                         'details': 'Debe indicar el id del centro y su tipo es un entero'}
                return Response(json.dumps(datos), mimetype="application/json")
            start = request.args.get('fecha_ini_calendario', type=str)
            if(not start):
                datos = {'status': 400, 'body': 'Bad Request',
                         'details': 'Debe indicar una fecha de inicio de tipo string en formato YYYY-MM-dd'}
                return Response(json.dumps(datos), mimetype="application/json")
            end = request.args.get('fecha_fin_calendario', type=str)
            if(not end):
                datos = {'status': 400, 'body': 'Bad Request',
                         'details': 'Debe indicar una fecha de fin de tipo string en formato YYYY-MM-dd'}
                return Response(json.dumps(datos), mimetype="application/json")
            centro = Centro.get_by_id(id_centro)
            if(centro == None):
                datos = {'status': 400, 'body': 'Bad Request',
                         'details': 'Ese centro no existe'}
                return Response(json.dumps(datos), mimetype="application/json")
            fecha_inicio = datetime.strptime(start, '%Y-%m-%d')
            fecha_fin = datetime.strptime(end, '%Y-%m-%d')
            if(fecha_inicio > fecha_fin):
                datos = {'status': 400, 'body': 'Bad Request',
                         'details': 'Rango incorrecto. La fecha de inicio no puede ser mayor a al fecha de fin'}
                return Response(json.dumps(datos), mimetype="application/json")
            turnos = Turno.get_by_id_centro(id_centro, fecha_inicio, fecha_fin)
            lista_turno = [unTurno.serializar for unTurno in turnos]
            datos = {'status': '200 OK', 'body': {'atributos': lista_turno}}
            return Response(json.dumps(datos), mimetype="application/json")
        except Exception as e:
            datos = {'status': 500, 'body': 'Internal Server Error'}
            return Response(json.dumps(datos), mimetype="application/json")
