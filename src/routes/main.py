from flask import Blueprint, render_template
from flask_login import login_required, current_user
from src.models.room import Room, RoomStatus
from src.models.reservation import Reservation, ReservationStatus
from src.models.guest import Guest
from datetime import datetime, timedelta
from src.extensions import db 
from sqlalchemy import func

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    # Obtener estadísticas de habitaciones
    total_rooms = Room.query.count()
    available_rooms = Room.query.filter_by(status=RoomStatus.AVAILABLE).count()
    occupied_rooms = Room.query.filter_by(status=RoomStatus.OCCUPIED).count()
    maintenance_rooms = Room.query.filter_by(status=RoomStatus.MAINTENANCE).count()

    # Obtener estadísticas de reservaciones
    today = datetime.utcnow()
    month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    total_reservations = Reservation.query.filter(
        Reservation.created_at >= month_start
    ).count()

    active_reservations = Reservation.query.filter(
        Reservation.status.in_([ReservationStatus.CONFIRMED, ReservationStatus.CHECKED_IN])
    ).count()

    # Calcular ingresos del mes
    monthly_revenue = db.session.query(
        func.sum(Reservation.total_price)
    ).filter(
        Reservation.created_at >= month_start,
        Reservation.status != ReservationStatus.CANCELLED
    ).scalar() or 0

    # Check-ins pendientes para hoy
    pending_checkins = Reservation.query.filter(
        Reservation.status == ReservationStatus.CONFIRMED,
        func.date(Reservation.check_in) == func.date(today)
    ).count()

    # Preparar estadísticas para la plantilla
    stats = {
        'total_rooms': total_rooms or 0,
        'available_rooms': available_rooms or 0,
        'occupied_rooms': occupied_rooms or 0,
        'maintenance_rooms': maintenance_rooms or 0,
        'total_reservations': total_reservations or 0,
        'active_reservations': active_reservations or 0,
        'monthly_revenue': monthly_revenue or 0,
        'pending_checkins': pending_checkins or 0,
        # Calcular porcentajes de manera segura
        'occupancy_rate': (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0,
        'availability_rate': (available_rooms / total_rooms * 100) if total_rooms > 0 else 0,
        'maintenance_rate': (maintenance_rooms / total_rooms * 100) if total_rooms > 0 else 0
    }

    # Obtener últimas reservaciones
    recent_reservations = Reservation.query.order_by(
        Reservation.created_at.desc()
    ).limit(5).all()

    return render_template(
        'index.html',
        stats=stats,
        recent_reservations=recent_reservations
    )