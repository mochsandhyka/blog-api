from sqlalchemy.dialects.postgresql import UUID
import uuid
from app import db
from app.models import user

class Address(db.Model):
    __tablename__ = 'tbl_address'
    id_address = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = db.Column(db.String(50),nullable = True)
    rt = db.Column(db.String(4),nullable = True)
    rw = db.Column(db.String(4),nullable = True)
    kelurahan_desa = db.Column(db.String(15),nullable = True)
    kecamatan = db.Column(db.String(15),nullable = True)
    user = db.relationship('User',backref='address',uselist=False)
    
