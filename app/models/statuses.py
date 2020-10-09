from app import db

class Statuses(db.Model):
    __tablename__ = "statuses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)

    @staticmethod 
    def find_by_id(id):
        return Statuses.query.filter_by(id=id).first()