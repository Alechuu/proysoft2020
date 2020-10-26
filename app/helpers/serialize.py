import json
import datetime
from flask import jsonify


def serializeSQLAlchemy(sqlresult,campos_no_deseados):
    parsed_sql_object = json.loads("{}")
    for column in sqlresult.__table__.columns:
        if (isinstance(getattr(sqlresult, str(column.key)),datetime.time)):
            objectToAppend = {str(column.key):(getattr(sqlresult, str(column.key))).strftime("%H:%M:%S")}
        else:
            if str(column.key) in campos_no_deseados:
                continue
            else:
                objectToAppend = {str(column.key):getattr(sqlresult, str(column.key))}   
        parsed_sql_object.update(objectToAppend)
    return (parsed_sql_object)
