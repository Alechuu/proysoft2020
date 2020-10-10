from app import db

class User(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    #@classmethod
    @staticmethod 
    def all():
        #sql = "SELECT * FROM users"
        #cursor = conn.cursor()
        #conn.execute(sql)
        #cursor.fetchall()
        #conn.execute(sql)
        return User.query.all()

    #@classmethod
    @staticmethod 
    def create(data):
        #sql = """
        #    INSERT INTO users (email, password, first_name, last_name)
        #    VALUES (%s, %s, %s, %s)
        #"""

        ##cursor = conn.cursor()
        #conn.execute(sql, list(data.values()))
        ##conn.commit()
        usuario = User(email=data.get("email"), password=data.get("password"), first_name=data.get("first_name"), last_name=data.get("last_name"))
        db.session.add(usuario)
        db.session.commit()
        return True

    #@classmethod
    @staticmethod 
    def find_by_email_and_pass(email, password):
        #sql = """
        #    SELECT * FROM users AS u
        #    WHERE u.email = %s AND u.password = %s
        #"""

        #cursor = conn.cursor()
        
        #res = conn.execute(sql, (email, password))
        #res.first()
        return User.query.filter_by(email=email,password=password).first()  

