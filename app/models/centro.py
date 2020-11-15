from app import db
from app.models.turno import Turno


class Centro(db.Model):
    __tablename__ = "centro_ayuda"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255),nullable=False)
    direccion = db.Column(db.String(255),nullable=False)
    telefono = db.Column(db.String(20),nullable=False)
    hora_apertura = db.Column(db.Time, nullable=True)
    hora_cierre = db.Column(db.Time, nullable=True)
    tipo_centro = db.Column(db.String(255), nullable=True)
    municipio = db.Column(db.String(255), nullable=True)
    sitio_web = db.Column(db.String(60),nullable=True)
    email = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.Boolean, default=False)
    latitud = db.Column(db.Numeric(9,6), nullable=True)
    longitud = db.Column(db.Numeric(9,6), nullable=True)
    path_pdf = db.Column(db.String(400), nullable=False)
    turnos = db.relationship("Turno", backref='centro', lazy=True)

    @staticmethod
    def get_all():
        return Centro.query.all()

    @staticmethod
    def get_all_api(pagina,maxCentros):
        totales = db.session.query(Centro).count()
        datos = Centro.query.paginate(pagina,maxCentros,False).items
        numPaginas = Centro.query.paginate(pagina,maxCentros,False).pages
        res = [totales,datos,numPaginas]
        return res
    
    @staticmethod
    def get_by_id(id_centro):
        try:
            return Centro.query.filter_by(id=id_centro).first()            
        except Exception as e:
            raise 
    
    @staticmethod
    def get_by_id_and_date(id_centro,fecha):
        try:
            return Centro.query.join(Centro.turnos).filter(Centro.id==id_centro,Turno.fecha==fecha).first()      
        except Exception as e:
            raise 


    def create(data,coords):
        nuevo_centro = Centro(
            nombre=data['nombre'],
            direccion=data['direccion'],
            telefono=data['telefono'],
            hora_apertura=data['hora_apertura'],
            hora_cierre=data['hora_cierre'],
            tipo_centro=data['tipo'],
            municipio=data['municipio'],
            sitio_web=data['sitio_web'],
            email=data['email'],
            estado=data['estado'],
            latitud=coords[0],
            longitud=coords[1]
        )

        try:
            db.session.add(nuevo_centro)
            db.session.commit()
            return nuevo_centro
        except Exception as e:
            db.session.rollback()
            raise
            return False

    @staticmethod       
    def agregarTurno(turno,centro):
        try:
            centro.turnos.append(turno)
            db.session.commit()
            return True
        except AttributeError as e:
            db.session.rollback()
            raise e
            return False
        except Exception as e:
            raise e
            return False

    @staticmethod 
    def cambiarEstado(id_centro):
        centro = db.session.query(Centro).filter(Centro.id==id_centro).first()
        #centro = Centro.find_by_username(nombre) como no tengo el campo username busco asi
        centro.estado = not centro.estado
        db.session.commit()
        return True

    @staticmethod
    def update(data):       
        try:
            micentro = db.session.query(Centro).filter(Centro.id==data.get('id_centro')).first()
            micentro.nombre = data.get("nombre")
            micentro.telefono = data.get("telefono")
            micentro.tipo_centro = data.get("tipo_centro")
            micentro.sitio_web = data.get("sitio_web")
            micentro.direccion = data.get("direccion")
            micentro.email = data.get("email")
            micentro.municipio = data.get("municipio")
            micentro.hora_apertura = data.get("hora_apertura")
            micentro.hora_cierre = data.get("hora_cierre")
            
            db.session.commit()
        except:
            db.session.rollback()
            raise
 
        return True

    @staticmethod 
    def delete(id_centro):
        micentro = db.session.query(Centro).filter(Centro.id==id_centro).first()
        if(micentro.turnos == []):
            db.session.delete(micentro)
            db.session.commit()
            return True
        else:
            return False


