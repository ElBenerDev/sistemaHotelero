from src.extensions import db
from datetime import datetime
from enum import Enum

class ReservationStatus(str, Enum):
    PENDING = "Pendiente"
    CONFIRMED = "Confirmada"
    CHECKED_IN = "Check-in"
    CHECKED_OUT = "Check-out"
    CANCELLED = "Cancelada"

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    check_in = db.Column(db.DateTime, nullable=False)
    check_out = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(ReservationStatus), default=ReservationStatus.PENDING)
    total_price = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    guest = db.relationship('Guest', backref=db.backref('reservations', lazy=True))
    room = db.relationship('Room', backref=db.backref('reservations', lazy=True))

    def __repr__(self):
        return f'<Reservation {self.id}>'