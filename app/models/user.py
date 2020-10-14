from app import db
from app.models.rol import Rol

usuario_tiene_rol = db.Table("usuario_tiene_rol",
    db.Column("rol_id", db.Integer, db.ForeignKey("rol.id"), primary_key=True),
    db.Column("usuario_id", db.Integer, db.ForeignKey("usuario.id"), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    roles = db.relationship("Rol", secondary=usuario_tiene_rol, lazy=True, backref=db.backref('usuarios', lazy=True))

    def __init__(self, id, username, email, password, activo, first_name, last_name, roles):
        self.id = id
        self.username = name
        self.email = email
        self.password = password
        self.activo = activo
        self.first_name = first_name
        self.last_name = last_name
        self.roles = roles


    @staticmethod 
    def all():
        return User.query.all()

    @staticmethod 
    def create(data):
        usuario = User(email=data.get("email"), password=data.get("password"), first_name=data.get("first_name"), last_name=data.get("last_name"))
        db.session.add(usuario)
        db.session.commit()
        return True
    
    @staticmethod 
    def delete(id_usuario):
        User.query.filter_by(id=id_usuario).delete()
        db.session.commit()
        return True

 
    @staticmethod
    def update(data):
       
        #miusuario = User.query.filter_by(id=data.get("id_usuario"))
        miusuario = User.find_by_username(data.get("username"))
        print(miusuario)
        miusuario.first_name = data.get("first_name")
        miusuario.last_name = data.get("last_name")
        miusuario.email = data.get("email")
        
        db.session.commit()
 
        return True
     

    @staticmethod 
    def find_by_username_and_pass(username, password):
        return User.query.filter_by(username=username,password=password).first()

    @staticmethod
    def find_by_username(username):
          return User.query.filter_by(username=username).first()


    