from app import db



class Permiso(db.Model):
    __tablename__ = 'permiso'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255),nullable=False)    

    @staticmethod
    def get_all():
        return Permiso.query.all()


    @staticmethod
    def get_by_name(nombre):
        return Permiso.query.filter_by(nombre=nombre).first()


    def set_nombre(self, nombre):
        self.nombre = nombre


    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()