from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from src.models.reservation import Reservation, ReservationStatus
from src.models.room import Room, RoomType, RoomStatus
from src.extensions import db
from sqlalchemy import func, case, extract, and_, distinct
from datetime import datetime, timedelta
import calendar

bp = Blueprint('reports', __name__, url_prefix='/reports')

@bp.route('/')
@login_required
def index():
    return render_template('reports/index.html')

@bp.route('/occupancy')
@login_required
def occupancy_stats():
    """Estadísticas de ocupación por tipo de habitación"""
    try:
        # Obtener el primer y último día del mes actual
        today = datetime.utcnow()
        first_day = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1], 
                               hour=23, minute=59, second=59)

        # Consulta para obtener habitaciones ocupadas
        occupancy_data = db.session.query(
            Room.type,
            func.count(distinct(Room.id)).label('total_rooms'),
            func.count(distinct(Reservation.id)).label('occupied_rooms')
        ).outerjoin(
            Reservation,
            and_(
                Room.id == Reservation.room_id,
                Reservation.status.in_([ReservationStatus.CONFIRMED, ReservationStatus.CHECKED_IN]),
                Reservation.check_in <= last_day,
                Reservation.check_out >= first_day
            )
        ).group_by(Room.type).all()

        result = []
        for room_type, total_rooms, occupied_rooms in occupancy_data:
            occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
            result.append({
                'type': room_type.value,
                'occupancy_rate': round(occupancy_rate, 2)
            })

        return jsonify(result)
    except Exception as e:
        print(f"Error en occupancy_stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/revenue')
@login_required
def revenue_stats():
    """Ingresos mensuales de los últimos 12 meses"""
    try:
        # Calcular fecha inicial (12 meses atrás)
        today = datetime.utcnow()
        start_date = (today - timedelta(days=365)).replace(day=1, hour=0, minute=0, second=0)

        # Consulta de ingresos mensuales
        revenue_data = db.session.query(
            func.strftime('%Y-%m', Reservation.check_in).label('month'),
            func.sum(Reservation.total_price).label('revenue')
        ).filter(
            Reservation.check_in >= start_date,
            Reservation.status != ReservationStatus.CANCELLED
        ).group_by(
            func.strftime('%Y-%m', Reservation.check_in)
        ).order_by(
            func.strftime('%Y-%m', Reservation.check_in)
        ).all()

        # Generar lista de todos los meses
        result = []
        for i in range(12):
            month_date = (today - timedelta(days=30*i)).replace(day=1)
            month_str = month_date.strftime('%Y-%m')
            
            # Buscar ingresos para este mes
            month_revenue = next(
                (item[1] for item in revenue_data if item[0] == month_str),
                0
            )
            
            result.insert(0, {
                'month': month_str,
                'revenue': float(month_revenue)
            })

        return jsonify(result)
    except Exception as e:
        print(f"Error en revenue_stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/dashboard-summary')
@login_required
def dashboard_summary():
    """Resumen para el dashboard"""
    try:
        today = datetime.utcnow()
        month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Consultas optimizadas
        current_month_stats = db.session.query(
            func.count(distinct(Reservation.id)).label('total_reservations'),
            func.sum(Reservation.total_price).label('total_revenue')
        ).filter(
            Reservation.check_in >= month_start,
            Reservation.status != ReservationStatus.CANCELLED
        ).first()

        # Reservaciones pendientes de check-in para hoy
        pending_checkins = Reservation.query.filter(
            Reservation.status == ReservationStatus.CONFIRMED,
            func.date(Reservation.check_in) == func.date(today)
        ).count()

        # Calcular ocupación actual
        occupancy_rate = calculate_current_occupancy()

        return jsonify({
            'total_reservations': current_month_stats[0] or 0,
            'total_revenue': float(current_month_stats[1] or 0),
            'occupancy_rate': occupancy_rate,
            'pending_checkins': pending_checkins
        })
    except Exception as e:
        print(f"Error en dashboard_summary: {str(e)}")
        return jsonify({'error': str(e)}), 500

def calculate_current_occupancy():
    """Calcula la tasa de ocupación actual"""
    try:
        today = datetime.utcnow()
        total_rooms = Room.query.count()
        
        occupied_rooms = db.session.query(func.count(distinct(Room.id))).join(
            Reservation
        ).filter(
            Reservation.check_in <= today,
            Reservation.check_out >= today,
            Reservation.status.in_([ReservationStatus.CONFIRMED, ReservationStatus.CHECKED_IN])
        ).scalar()

        return round((occupied_rooms / total_rooms * 100), 2) if total_rooms > 0 else 0
    except Exception as e:
        print(f"Error calculando ocupación: {str(e)}")
        return 0