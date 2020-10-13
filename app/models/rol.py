from app import db
from app.models.permiso import Permiso

rol_tiene_permiso = db.Table("rol_tiene_permiso",
    db.Column("rol_id", db.Integer, db.ForeignKey("rol.id"), primary_key=True),
    db.Column("permiso_id", db.Integer, db.ForeignKey("permiso.id"), primary_key=True)
)

class Rol(db.Model):
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255),nullable=False)   
    permisos = db.relationship("Permiso", secondary=rol_tiene_permiso, lazy=True, backref=db.backref('roles', lazy=True)) 

    @staticmethod
    def get_all():
        return Rol.query.all()
    
    def set_nombre(self, nombre):
        self.nombre = nombre

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()