from src.extensions import db
from datetime import datetime
from enum import Enum

class DocumentType(str, Enum):
    INE = 'INE'
    PASSPORT = 'Pasaporte'
    FOREIGN_ID = 'Carné de Extranjería'
    OTHER = 'Otro'

class Guest(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    id_type = db.Column(db.Enum(DocumentType), nullable=True)
    id_number = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con reservaciones
    reservations = db.relationship(
        'Reservation',
        back_populates='guest',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<Guest {self.first_name} {self.last_name}>'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'