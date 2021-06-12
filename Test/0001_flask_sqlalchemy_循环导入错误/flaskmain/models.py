from . import db



class User(db.Model):
    id = db.Column(db.Ingeger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), unique=True)
