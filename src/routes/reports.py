from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from src.models.reservation import Reservation, ReservationStatus
from src.models.room import Room, RoomType, RoomStatus
from src.extensions import db
from sqlalchemy import func, case, extract
from datetime import datetime, timedelta

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
        stats = db.session.query(
            Room.type,
            func.count(Room.id).label('total'),
            func.sum(case([(Room.status == RoomStatus.OCCUPIED, 1)], else_=0)).label('occupied')
        ).group_by(Room.type).all()
        
        result = []
        for room_type, total, occupied in stats:
            result.append({
                'type': room_type.value,
                'total': total,
                'occupied': occupied or 0,  # Convertir None a 0
                'occupancy_rate': ((occupied or 0) / total * 100) if total > 0 else 0
            })
        
        return jsonify(result)
    except Exception as e:
        print(f"Error en occupancy_stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/revenue')
@login_required
def revenue_stats():
    """Ingresos por mes"""
    try:
        last_6_months = datetime.utcnow() - timedelta(days=180)
        
        # Consulta modificada para SQLite
        stats = db.session.query(
            extract('year', Reservation.check_in).label('year'),
            extract('month', Reservation.check_in).label('month'),
            func.sum(Reservation.total_price).label('revenue')
        ).filter(
            Reservation.check_in >= last_6_months,
            Reservation.status != ReservationStatus.CANCELLED
        ).group_by(
            extract('year', Reservation.check_in),
            extract('month', Reservation.check_in)
        ).order_by(
            extract('year', Reservation.check_in),
            extract('month', Reservation.check_in)
        ).all()
        
        result = []
        for year, month, revenue in stats:
            # Formatear fecha
            month_str = f"{int(year):04d}-{int(month):02d}"
            result.append({
                'month': month_str,
                'revenue': float(revenue or 0)
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
        
        # Estadísticas del mes actual
        monthly_stats = {
            'total_reservations': Reservation.query.filter(
                Reservation.check_in >= month_start
            ).count(),
            
            'total_revenue': db.session.query(
                func.sum(Reservation.total_price)
            ).filter(
                Reservation.check_in >= month_start,
                Reservation.status != ReservationStatus.CANCELLED
            ).scalar() or 0,
            
            'occupancy_rate': calculate_current_occupancy(),
            
            'pending_checkins': Reservation.query.filter(
                Reservation.status == ReservationStatus.CONFIRMED,
                Reservation.check_in >= today,
                Reservation.check_in < today + timedelta(days=1)
            ).count()
        }
        
        return jsonify(monthly_stats)
    except Exception as e:
        print(f"Error en dashboard_summary: {str(e)}")
        return jsonify({'error': str(e)}), 500

def calculate_current_occupancy():
    """Calcula la tasa de ocupación actual"""
    try:
        total_rooms = Room.query.count()
        occupied_rooms = Room.query.filter_by(status=RoomStatus.OCCUPIED).count()
        return (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
    except Exception as e:
        print(f"Error calculando ocupación: {str(e)}")
        return 0