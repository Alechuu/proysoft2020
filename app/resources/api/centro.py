from flask import Response

import json
from app.helpers.serialize_centros import serializeSQLAlchemy
from app.models.configuracion import Configuracion
from app.models.centro import Centro



def api_get_all(pagina):
    miConfiguracion = Configuracion.get_first()
    centros = Centro.get_all_api(int(pagina),miConfiguracion.paginado)
    if(centros[1] == []):
        datos = {'status':400,'body':'Número de página inválido','pagina_maxima':centros[2]}
        return Response(json.dumps(datos), mimetype='application/json')
    parsed_list = []
    for centro in centros[1]:
        parsed_list.append(serializeSQLAlchemy(centro))
    datos = {'status':200,'centros':parsed_list,'total':centros[0],'pagina':int(pagina)}
    return Response(json.dumps(datos), mimetype='application/json')