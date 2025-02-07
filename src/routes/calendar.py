from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from src.models.room import Room
from src.models.reservation import Reservation
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
    reservations = Reservation.query.all()
    events = []
    
    for reservation in reservations:
        events.append({
            'id': reservation.id,
            'title': f'{reservation.guest.full_name} - {reservation.room.number}',
            'start': reservation.check_in.isoformat(),
            'end': reservation.check_out.isoformat(),
            'room_id': reservation.room_id,
            'room_number': reservation.room.number,
            'guest_name': reservation.guest.full_name,
            'check_in': reservation.check_in.strftime('%Y-%m-%d %H:%M'),
            'check_out': reservation.check_out.strftime('%Y-%m-%d %H:%M'),
            'status': reservation.status.value,
            'total_price': f"{reservation.total_price:.2f}",
            'notes': reservation.notes
        })
    
    return jsonify(events)