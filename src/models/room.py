from src.extensions import db
from datetime import datetime
from enum import Enum

class RoomType(str, Enum):
    SINGLE = 'Individual'
    DOUBLE = 'Doble'
    SUITE = 'Suite'
    FAMILY = 'Familiar'

class RoomStatus(str, Enum):
    AVAILABLE = 'Disponible'
    OCCUPIED = 'Ocupada'
    MAINTENANCE = 'Mantenimiento'
    CLEANING = 'Limpieza'

class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum(RoomType), nullable=False)
    status = db.Column(db.Enum(RoomStatus), default=RoomStatus.AVAILABLE)
    price_per_night = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    reservations = db.relationship(
        'Reservation',
        back_populates='room',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<Room {self.number} - {self.type.value}>'