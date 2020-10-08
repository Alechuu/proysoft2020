import pymysql

from flask import current_app
from flask import g
from flask import cli
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker

def connection():
    if "db_conn" not in g:
        conf = current_app.config
        engine = create_engine(conf["SQLALCHEMY_DATABASE_URI"])
        #Session = sessionmaker(bind=engine)
        g.db_conn = engine.connect()
        
        # pymysql.connect(
        #     host=conf["DB_HOST"],
        #     user=conf["DB_USER"],
        #     password=conf["DB_PASS"],
        #     db=conf["DB_NAME"],
        #     cursorclass=pymysql.cursors.DictCursor,
        # )

    return g.db_conn


def close(e=None):
    conn = g.pop("db_conn", None)

    if conn is not None:
        conn.close()


def init_app(app):
    #app.teardown_appcontext() tells Flask to call that function when cleaning up after returning the response.
    #El parámetro "close" es la función de arriba!
    app.teardown_appcontext(close)
