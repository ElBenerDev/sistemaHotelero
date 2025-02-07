from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from src.models.reservation import Reservation, ReservationStatus
from src.models.room import Room, RoomStatus
from src.models.guest import Guest
from src.extensions import db
from datetime import datetime
import pytz

bp = Blueprint('reservations', __name__, url_prefix='/reservations')

@bp.route('/')
@login_required
def index():
    reservations = Reservation.query.order_by(Reservation.created_at.desc()).all()
    return render_template('reservations/index.html', 
                         reservations=reservations, 
                         ReservationStatus=ReservationStatus)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        try:
            # Convertir fechas del formato ISO a datetime
            check_in = datetime.fromisoformat(request.form['check_in'].replace('T', ' '))
            check_out = datetime.fromisoformat(request.form['check_out'].replace('T', ' '))
            
            # Validar fechas
            if check_in >= check_out:
                flash('La fecha de salida debe ser posterior a la fecha de entrada', 'danger')
                return redirect(url_for('reservations.new'))

            # Crear la reservación
            reservation = Reservation(
                guest_id=request.form['guest_id'],
                room_id=request.form['room_id'],
                check_in=check_in,
                check_out=check_out,
                status=ReservationStatus.PENDING,
                notes=request.form.get('notes', '')
            )

            # Calcular el total
            room = Room.query.get(request.form['room_id'])
            reservation.total_price = reservation.calculate_total(room.price_per_night)

            db.session.add(reservation)
            
            # Actualizar estado de la habitación
            room.status = RoomStatus.OCCUPIED
            
            db.session.commit()

            flash('Reservación creada exitosamente', 'success')
            return redirect(url_for('reservations.index'))

        except ValueError as e:
            flash(f'Error al crear la reservación: {str(e)}', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la reservación: {str(e)}', 'danger')

    rooms = Room.query.filter_by(status=RoomStatus.AVAILABLE).all()
    return render_template('reservations/new.html', 
                         rooms=rooms, 
                         ReservationStatus=ReservationStatus)

@bp.route('/<int:id>')
@login_required
def view(id):
    reservation = Reservation.query.get_or_404(id)
    return render_template('reservations/view.html', 
                         reservation=reservation,
                         ReservationStatus=ReservationStatus)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    reservation = Reservation.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Actualizar estado de la habitación anterior si cambió
            if int(request.form['room_id']) != reservation.room_id:
                old_room = Room.query.get(reservation.room_id)
                old_room.status = RoomStatus.AVAILABLE
                new_room = Room.query.get(request.form['room_id'])
                new_room.status = RoomStatus.OCCUPIED
            
            # Convertir fechas del formato ISO a datetime
            check_in = datetime.fromisoformat(request.form['check_in'].replace('T', ' '))
            check_out = datetime.fromisoformat(request.form['check_out'].replace('T', ' '))
            
            # Validar fechas
            if check_in >= check_out:
                flash('La fecha de salida debe ser posterior a la fecha de entrada', 'danger')
                return redirect(url_for('reservations.edit', id=id))

            # Actualizar reservación
            reservation.guest_id = request.form['guest_id']
            reservation.room_id = request.form['room_id']
            reservation.check_in = check_in
            reservation.check_out = check_out
            
            # Convertir el string del estado a enum
            new_status = getattr(ReservationStatus, request.form['status'])
            reservation.status = new_status
            
            reservation.notes = request.form.get('notes', '')
            
            # Recalcular total
            room = Room.query.get(request.form['room_id'])
            reservation.total_price = reservation.calculate_total(room.price_per_night)
            
            # Actualizar estado de la habitación según el nuevo estado de la reservación
            if new_status == ReservationStatus.CANCELLED:
                room.status = RoomStatus.AVAILABLE
            elif new_status in [ReservationStatus.CONFIRMED, ReservationStatus.CHECKED_IN]:
                room.status = RoomStatus.OCCUPIED
            elif new_status == ReservationStatus.CHECKED_OUT:
                room.status = RoomStatus.CLEANING
            
            db.session.commit()
            flash('Reservación actualizada exitosamente', 'success')
            return redirect(url_for('reservations.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la reservación: {str(e)}', 'danger')
    
    rooms = Room.query.all()
    return render_template('reservations/edit.html', 
                         reservation=reservation,
                         rooms=rooms,
                         ReservationStatus=ReservationStatus)

@bp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel(id):
    reservation = Reservation.query.get_or_404(id)
    if reservation.status == ReservationStatus.PENDING:
        try:
            reservation.status = ReservationStatus.CANCELLED
            # Liberar la habitación
            room = Room.query.get(reservation.room_id)
            room.status = RoomStatus.AVAILABLE
            
            db.session.commit()
            flash('Reservación cancelada exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al cancelar la reservación: {str(e)}', 'danger')
    else:
        flash('Solo se pueden cancelar reservaciones pendientes', 'warning')
    
    return redirect(url_for('reservations.index'))

@bp.route('/<int:id>/check-in', methods=['POST'])
@login_required
def check_in(id):
    reservation = Reservation.query.get_or_404(id)
    if reservation.status == ReservationStatus.CONFIRMED:
        try:
            reservation.status = ReservationStatus.CHECKED_IN
            db.session.commit()
            flash('Check-in realizado exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al realizar check-in: {str(e)}', 'danger')
    else:
        flash('Solo se puede hacer check-in de reservaciones confirmadas', 'warning')
    
    return redirect(url_for('reservations.view', id=id))

@bp.route('/<int:id>/check-out', methods=['POST'])
@login_required
def check_out(id):
    reservation = Reservation.query.get_or_404(id)
    if reservation.status == ReservationStatus.CHECKED_IN:
        try:
            reservation.status = ReservationStatus.CHECKED_OUT
            # Liberar la habitación
            room = Room.query.get(reservation.room_id)
            room.status = RoomStatus.CLEANING
            
            db.session.commit()
            flash('Check-out realizado exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al realizar check-out: {str(e)}', 'danger')
    else:
        flash('Solo se puede hacer check-out de reservaciones con check-in', 'warning')
    
    return redirect(url_for('reservations.view', id=id))