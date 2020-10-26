import json

from flask import Response
from flask_restful import Resource

from app.helpers.serialize import serializeSQLAlchemy
from app.models.configuracion import Configuracion
from app.models.centro import Centro



class AllCentros(Resource):
    
    def get(self,pagina):
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

   