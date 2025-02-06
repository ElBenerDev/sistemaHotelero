from src.extensions import db
from src.models.reservation import Reservation, ReservationStatus
from datetime import datetime, timedelta

def cleanup_expired_reservations():
    """Cancela automáticamente las reservaciones pendientes expiradas"""
    expiration_time = datetime.utcnow() - timedelta(days=1)
    expired = Reservation.query.filter(
        Reservation.status == ReservationStatus.PENDING,
        Reservation.created_at <= expiration_time
    ).all()
    
    for reservation in expired:
        reservation.status = ReservationStatus.CANCELLED
    
    db.session.commit()