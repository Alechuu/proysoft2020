from app import db

class Configuracion(db.Model):
    __tablename__ = 'configuracion'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255),nullable=False)
    descripcion = db.Column(db.String(255))
    email = db.Column(db.String(255))
    paginado = db.Column(db.Integer, default=10)
    habilitado = db.Column(db.Boolean, default=False)

    @staticmethod
    def get_first():
        return Configuracion.query.first()