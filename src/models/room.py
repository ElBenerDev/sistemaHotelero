from src.extensions import db
from enum import Enum

class RoomType(str, Enum):
    SINGLE = "Individual"
    DOUBLE = "Doble"
    SUITE = "Suite"
    FAMILY = "Familiar"

class RoomStatus(str, Enum):
    AVAILABLE = "Disponible"
    OCCUPIED = "Ocupada"
    MAINTENANCE = "Mantenimiento"
    CLEANING = "Limpieza"

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)
    type = db.Column(db.Enum(RoomType), nullable=False)
    status = db.Column(db.Enum(RoomStatus), default=RoomStatus.AVAILABLE)
    price = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    floor = db.Column(db.Integer)

    def __repr__(self):
        return f'<Room {self.number}>'