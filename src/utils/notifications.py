from datetime import datetime, timedelta
from src.models.reservation import Reservation, ReservationStatus
from src.extensions import db

def get_upcoming_checkouts():
    """Obtiene las reservaciones que tienen check-out en las próximas 24 horas"""
    tomorrow = datetime.utcnow() + timedelta(days=1)
    return Reservation.query.filter(
        Reservation.status == ReservationStatus.CHECKED_IN,
        Reservation.check_out <= tomorrow
    ).all()

def get_upcoming_checkins():
    """Obtiene las reservaciones que tienen check-in en las próximas 24 horas"""
    tomorrow = datetime.utcnow() + timedelta(days=1)
    return Reservation.query.filter(
        Reservation.status == ReservationStatus.CONFIRMED,
        Reservation.check_in <= tomorrow
    ).all()