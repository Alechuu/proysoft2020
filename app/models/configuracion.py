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


    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()


    def set_titulo(self, titulo):
        self.titulo = titulo


    def set_descripcion(self, descripcion):
        self.descripcion = descripcion


    def set_email(self, email):
        self.email = email


    def set_paginado(self, paginado):
        self.paginado = paginado
        
           
    def set_habilitado(self, habilitado):
        self.habilitado = habilitado
