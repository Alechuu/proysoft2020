from app import db

class Categories(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)

    @staticmethod 
    def find_by_id(id):
        return Categories.query.filter_by(id=id).first()