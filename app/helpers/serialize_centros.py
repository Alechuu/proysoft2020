import json
import datetime
from flask import jsonify


def serializeSQLAlchemy(sqlresult):
    parsed_sql_object = json.loads("{}")
    for column in sqlresult.__table__.columns:
        if (isinstance(getattr(sqlresult, str(column.key)),datetime.time)):
            objectToAppend = {str(column.key):(getattr(sqlresult, str(column.key))).strftime("%H:%M:%S")}
        else:
            key = str(column.key)
            if(key=='latitud'):
                continue
            if(key=='longitud'):
                continue
            if(key=='estado'):
                continue
            if(key=='id_municipio'):
                continue
            if(key=='id_tipo_centro'):
                continue
            else:
                objectToAppend = {str(column.key):getattr(sqlresult, str(column.key))}   
        parsed_sql_object.update(objectToAppend)
    return (parsed_sql_object)
