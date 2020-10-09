from flask import current_app
from flask import g
from flask import cli
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

db = SQLAlchemy()

def connection():
    if "db_conn" not in g:
        conf = current_app.config
        engine = create_engine(conf["SQLALCHEMY_DATABASE_URI"])
        g.db_conn = engine.connect()

    return g.db_conn


def close(e=None):
    conn = g.pop("db_conn", None)

    if conn is not None:
        conn.close()


def init_app(app):
    #app.teardown_appcontext() tells Flask to call that function when cleaning up after returning the response.
    #El parámetro "close" es la función de arriba!
    app.teardown_appcontext(close)
