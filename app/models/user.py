from app import db
from app.models import address


class User(db.Model):
    id_user = db.Column(db.BigInteger,primary_key=True,autoincrement=True)
    name = db.Column(db.String(40),nullable=False)
    address = db.relationship('address',backref='user')
