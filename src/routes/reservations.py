from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from src.extensions import db
from src.models.reservation import Reservation, ReservationStatus
from src.models.room import Room
from src.models.guest import Guest
from datetime import datetime

bp = Blueprint('reservations', __name__, url_prefix='/reservations')

@bp.route('/')
@login_required
def index():
    reservations = Reservation.query.order_by(Reservation.created_at.desc()).all()
    return render_template('reservations/index.html', reservations=reservations)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    rooms = Room.query.all()
    guests = Guest.query.all()
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            guest_id = request.form.get('guest_id')
            room_id = request.form.get('room_id')
            check_in = datetime.strptime(request.form.get('check_in'), '%Y-%m-%dT%H:%M')
            check_out = datetime.strptime(request.form.get('check_out'), '%Y-%m-%dT%H:%M')
            status = ReservationStatus[request.form.get('status', 'PENDING')]
            total_price = float(request.form.get('total_price', 0))
            notes = request.form.get('notes', '')

            reservation = Reservation(
                guest_id=guest_id,
                room_id=room_id,
                check_in=check_in,
                check_out=check_out,
                status=status,
                total_price=total_price,
                notes=notes
            )

            db.session.add(reservation)
            db.session.commit()
            flash('Reservación creada exitosamente.', 'success')
            return redirect(url_for('reservations.index'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la reservación: {str(e)}', 'danger')

    return render_template('reservations/add.html', 
                         rooms=rooms, 
                         guests=guests,
                         statuses=ReservationStatus)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    reservation = Reservation.query.get_or_404(id)
    rooms = Room.query.all()
    guests = Guest.query.all()
    
    if request.method == 'POST':
        try:
            reservation.guest_id = request.form.get('guest_id')
            reservation.room_id = request.form.get('room_id')
            reservation.check_in = datetime.strptime(request.form.get('check_in'), '%Y-%m-%dT%H:%M')
            reservation.check_out = datetime.strptime(request.form.get('check_out'), '%Y-%m-%dT%H:%M')
            reservation.status = ReservationStatus[request.form.get('status')]
            reservation.total_price = float(request.form.get('total_price', 0))
            reservation.notes = request.form.get('notes', '')

            db.session.commit()
            flash('Reservación actualizada exitosamente.', 'success')
            return redirect(url_for('reservations.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la reservación: {str(e)}', 'danger')

    return render_template('reservations/edit.html',
                         reservation=reservation,
                         rooms=rooms,
                         guests=guests,
                         statuses=ReservationStatus)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    reservation = Reservation.query.get_or_404(id)
    try:
        db.session.delete(reservation)
        db.session.commit()
        flash('Reservación eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la reservación: {str(e)}', 'danger')
    return redirect(url_for('reservations.index'))