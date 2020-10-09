from app import db
from app.models.statuses import Statuses
from app.models.categories import Categories

class Issue(db.Model):
    __tablename__ = "issues"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256))
    description = db.Column(db.String(256))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False) 
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False) 
    
    #@classmethod
    @staticmethod  
    def get_all():
        return Issue.query.all()

    """ @classmethod
    def all(cls, conn):
        sql = "SELECT * FROM issues"

        #cursor = conn.cursor()
        #cursor.execute(sql)

        return conn.execute(sql)#cursor.fetchall() """

    #@classmethod
    @staticmethod  
    def create(data):
        #sql = """
        #    INSERT INTO issues (email, description, category_id, status_id)
        #    VALUES (%s, %s, %s, %s)
        #"""

        #cursor = conn.cursor()
        #conn.execute(sql, list(data.values()))
        #conn.commit()
        cat = Categories.find_by_id(data.get("category_id"))
        status = Statuses.find_by_id(data.get("status_id"))
        iss = Issue(email=data.get("email"), description=data.get("description"), category_id=cat.id, status_id=status.id)
        db.session.add(iss)
        db.session.commit()

        return True
