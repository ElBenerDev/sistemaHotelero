from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from src.models.room import Room, RoomStatus
from src.models.reservation import Reservation, ReservationStatus
from src.extensions import db  # Agregar esta importación
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)

def get_upcoming_checkins():
    """Obtiene las reservaciones que tienen check-in en las próximas 24 horas"""
    tomorrow = datetime.utcnow() + timedelta(days=1)
    return Reservation.query.filter(
        Reservation.status == ReservationStatus.CONFIRMED,
        Reservation.check_in <= tomorrow
    ).all()

def get_upcoming_checkouts():
    """Obtiene las reservaciones que tienen check-out en las próximas 24 horas"""
    tomorrow = datetime.utcnow() + timedelta(days=1)
    return Reservation.query.filter(
        Reservation.status == ReservationStatus.CHECKED_IN,
        Reservation.check_out <= tomorrow
    ).all()

def get_monthly_revenue():
    """Calcula los ingresos del mes actual"""
    start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return db.session.query(func.sum(Reservation.total_price))\
        .filter(
            Reservation.check_in >= start_of_month,
            Reservation.status != ReservationStatus.CANCELLED
        ).scalar() or 0

def calculate_occupancy_rate():
    """Calcula la tasa de ocupación actual"""
    total_rooms = Room.query.count()
    occupied_rooms = Room.query.filter_by(status=RoomStatus.OCCUPIED).count()
    return (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0

@bp.route('/')
@login_required
def index():
    # Obtener estadísticas reales de la base de datos
    stats = {
        'rooms_available': Room.query.filter_by(status=RoomStatus.AVAILABLE).count(),
        'active_reservations': Reservation.query.filter_by(status=ReservationStatus.CHECKED_IN).count(),
        'total_rooms': Room.query.count(),
        'maintenance_rooms': Room.query.filter_by(status=RoomStatus.MAINTENANCE).count()
    }
    
    # Obtener las reservaciones más recientes
    recent_reservations = Reservation.query\
        .order_by(Reservation.created_at.desc())\
        .limit(5)\
        .all()
    
    return render_template('index.html', 
                         stats=stats, 
                         recent_reservations=recent_reservations)

@bp.route('/dashboard-stats')
@login_required
def dashboard_stats():
    today = datetime.utcnow()
    stats = {
        'upcoming_checkins': len(get_upcoming_checkins()),
        'upcoming_checkouts': len(get_upcoming_checkouts()),
        'monthly_revenue': get_monthly_revenue(),
        'occupancy_rate': calculate_occupancy_rate()
    }
    return jsonify(stats)