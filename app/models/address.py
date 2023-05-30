from app import db
from app.models import user

class Address(db.Model):
    id_address = db.Column(db.BigInteger,primary_key  = True,autoincrement = True)
    address = db.Column(db.String(50),nullable = False)
    rt = db.Column(db.String(3),nullable = False)
    rw = db.Column(db.String(3),nullable = False)
    keldes = db.Column(db.String(15),nullable = False)
    kec = db.Column(db.String(15),nullable = False)
    id_user = db.Column(db.BigInteger,db.ForeignKey('user.id_user'))

