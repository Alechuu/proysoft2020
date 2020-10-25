import json

from flask import jsonify


def serializeSQLAlchemy(sqlresult):
    parsed_sql_object = json.loads("{}")
    for column in sqlresult.__table__.columns:
        objectToAppend = {str(column.key):getattr(sqlresult, str(column.key))}
        parsed_sql_object.update(objectToAppend) 
    return jsonify(parsed_sql_object)
