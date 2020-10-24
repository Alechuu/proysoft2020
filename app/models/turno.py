from app import db

class Turno(db.Model):
    __tablename__ = "turnos"
    id = db.Column(db.Integer, primary_key=True)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    email_visitante = db.Column(db.String(255),nullable=False)
    telefono_visitante = db.Column(db.String(20),nullable=False)
    id_centro_ayuda = db.Column(db.Integer, db.ForeignKey('centro_ayuda.id'), nullable=False)

    @staticmethod
    def get_all():
        return Turno.query.all()