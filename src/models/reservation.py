from src.extensions import db
from datetime import datetime
from enum import Enum

class ReservationStatus(str, Enum):
    PENDING = "Pendiente"
    CONFIRMED = "Confirmada"
    CHECKED_IN = "Check-in"
    CHECKED_OUT = "Check-out"
    CANCELLED = "Cancelada"

    @classmethod
    def from_string(cls, status_str):
        """Convierte un string al enum correspondiente"""
        try:
            return cls[status_str]
        except KeyError:
            raise ValueError(f"'{status_str}' no es un estado válido")

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    check_in = db.Column(db.DateTime, nullable=False)
    check_out = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(ReservationStatus), default=ReservationStatus.PENDING)
    total_price = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    guest = db.relationship('Guest', back_populates='reservations')
    room = db.relationship('Room', back_populates='reservations')

    def __repr__(self):
        return f'<Reservation {self.id}>'

    @property
    def nights(self):
        """Calcula el número de noches de la reservación"""
        if self.check_in and self.check_out:
            return (self.check_out - self.check_in).days
        return 0

    def calculate_total(self, room_price):
        """Calcula el total de la reservación"""
        return self.nights * room_price if self.nights > 0 else 0

    def validate_dates(self):
        """Valida las fechas de la reservación"""
        if self.check_in >= self.check_out:
            raise ValueError("La fecha de salida debe ser posterior a la fecha de entrada")
        
        if self.check_in.date() < datetime.utcnow().date():
            raise ValueError("La fecha de entrada no puede ser anterior a hoy")

    def can_transition_to(self, new_status):
        """Valida si se puede cambiar al nuevo estado"""
        valid_transitions = {
            ReservationStatus.PENDING: [ReservationStatus.CONFIRMED, ReservationStatus.CANCELLED],
            ReservationStatus.CONFIRMED: [ReservationStatus.CHECKED_IN, ReservationStatus.CANCELLED],
            ReservationStatus.CHECKED_IN: [ReservationStatus.CHECKED_OUT],
            ReservationStatus.CHECKED_OUT: [],
            ReservationStatus.CANCELLED: []
        }
        return new_status in valid_transitions.get(self.status, [])