from sqlalchemy.dialects.postgresql import UUID
import uuid
from app import db
from app.models import address

class User(db.Model):
    __tablename__ = 'tbl_user'
    id_user = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(40), nullable=False)
    created_at = db.Column(db.DateTime)
    id_address = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_address.id_address'))


