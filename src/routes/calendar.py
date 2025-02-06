from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
from src.models.reservation import Reservation, ReservationStatus
from src.models.room import Room
from datetime import datetime

bp = Blueprint('calendar', __name__, url_prefix='/calendar')

@bp.route('/')
@login_required
def index():
    rooms = Room.query.order_by(Room.number).all()
    return render_template('calendar/index.html', rooms=rooms)

@bp.route('/events')
@login_required
def get_events():
    start = request.args.get('start')
    end = request.args.get('end')
    room_id = request.args.get('room_id')
    status = request.args.get('status')
    
    query = Reservation.query
    
    if start and end:
        start_date = datetime.fromisoformat(start.replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(end.replace('Z', '+00:00'))
        query = query.filter(
            Reservation.check_in <= end_date,
            Reservation.check_out >= start_date
        )
    
    if room_id:
        query = query.filter(Reservation.room_id == room_id)
        
    if status:
        query = query.filter(Reservation.status == ReservationStatus[status])
    
    reservations = query.all()
    
    events = []
    status_colors = {
        ReservationStatus.PENDING: '#ffc107',
        ReservationStatus.CONFIRMED: '#0d6efd',
        ReservationStatus.CHECKED_IN: '#198754',
        ReservationStatus.CHECKED_OUT: '#6c757d',
        ReservationStatus.CANCELLED: '#dc3545'
    }
    
    for reservation in reservations:
        events.append({
            'id': reservation.id,
            'title': f'Hab {reservation.room.number} - {reservation.guest.full_name}',
            'start': reservation.check_in.isoformat(),
            'end': reservation.check_out.isoformat(),
            'backgroundColor': status_colors.get(reservation.status, '#6c757d'),
            'borderColor': status_colors.get(reservation.status, '#6c757d'),
            'textColor': '#ffffff',
            'extendedProps': {
                'room_number': reservation.room.number,
                'guest_name': reservation.guest.full_name,
                'status': reservation.status.value,
                'total_price': f"${reservation.total_price:.2f}",
                'notes': reservation.notes
            }
        })
    
    return jsonify(events)