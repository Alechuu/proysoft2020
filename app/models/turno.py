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
    
    @staticmethod
    def get_by_id(id_turno):
        return Turno.query.get(id_turno)
    
    @staticmethod
    def get_by_id_centro(id_centro, fecha_inicio, fecha_fin):
        return Turno.query.filter(Turno.fecha.between(fecha_inicio, fecha_fin)).filter_by(id_centro_ayuda=id_centro).all()

    @property
    def serializar(self):
        return {
            'id':self.id,
            'hora_inicio':self.dump_datetime(self.fecha, self.hora_inicio),
            'hora_fin':self.dump_datetime(self.fecha, self.hora_fin),
            'fecha':self.dump_date(self.fecha),
            'email_visitante':self.email_visitante,
            'telefono_visitante':self.telefono_visitante,
            'id_centro_ayuda':self.id_centro_ayuda
            }

    @staticmethod
    def dump_datetime(fecha, hora):
       """Deserialize datetime object into string form for JSON processing."""
       if fecha is None:
           return None
       if hora is None:
           return None
       return fecha.strftime("%Y-%m-%d") +' ' + hora.strftime("%H:%M:%S")
    
    @staticmethod
    def dump_date(fecha):
        if fecha is None:
           return None
        return fecha.strftime("%Y-%m-%d")

    @staticmethod
    def new(data):
        nuevo_turno = Turno(
            hora_inicio = data['hora_inicio'],
            hora_fin = data['hora_fin'],
            fecha = data['fecha'],
            email_visitante = data['email_visitante'],
            telefono_visitante = data['telefono_visitante']
        )
        return nuevo_turno
    
    @staticmethod
    def get_by_hour_and_date(hour,date,id_centro):
        return Turno.query.filter(Turno.hora_inicio==hour, Turno.fecha==date, Turno.id_centro_ayuda==id_centro).first()
    
    @staticmethod
    def borrar_turno(id_turno):
        turno = Turno.query.get(id_turno)
        db.session.delete(turno)
        db.session.commit()
        return True

    @staticmethod
    def update(unTurno, data):
        unTurno.hora_inicio = data['hora_inicio'],
        unTurno.hora_fin = data['hora_fin'],
        unTurno.fecha = data['fecha'],
        unTurno.email_visitante = data['email_visitante'],
        unTurno.telefono_visitante = data['telefono_visitante']
        db.session.commit()
        return True
