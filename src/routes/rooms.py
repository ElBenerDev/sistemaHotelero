from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from src.models.room import Room, RoomType, RoomStatus
from src.extensions import db

bp = Blueprint('rooms', __name__, url_prefix='/rooms')

@bp.route('/')
@login_required
def index():
    # Obtener parámetros de filtro
    floor = request.args.get('floor', type=int)
    room_type = request.args.get('type')
    status = request.args.get('status')
    
    # Query base
    query = Room.query
    
    # Aplicar filtros si existen
    if floor is not None:
        query = query.filter(Room.floor == floor)
    if room_type:
        query = query.filter(Room.type == RoomType[room_type])
    if status:
        query = query.filter(Room.status == RoomStatus[status])
    
    # Ordenar por número de habitación
    rooms = query.order_by(Room.number).all()
    
    # Obtener lista de pisos únicos para el filtro
    floors = sorted(set(room.floor for room in Room.query.all()))
    
    return render_template(
        'rooms/index.html',
        rooms=rooms,
        floors=floors,
        room_types=RoomType,
        room_statuses=RoomStatus,
        selected_floor=floor,
        selected_type=room_type,
        selected_status=status
    )

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        try:
            room = Room(
                number=request.form['number'],
                floor=int(request.form['floor']),
                type=RoomType[request.form['type']],
                status=RoomStatus[request.form['status']],
                price_per_night=float(request.form['price_per_night']),
                capacity=int(request.form['capacity']),
                description=request.form['description']
            )
            db.session.add(room)
            db.session.commit()
            flash('Habitación agregada correctamente.', 'success')
            return redirect(url_for('rooms.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar la habitación: {str(e)}', 'danger')
            return redirect(url_for('rooms.add'))

    return render_template('rooms/add.html', room_types=RoomType, room_statuses=RoomStatus)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    room = Room.query.get_or_404(id)
    if request.method == 'POST':
        try:
            room.number = request.form['number']
            room.floor = int(request.form['floor'])
            room.type = RoomType[request.form['type']]
            room.status = RoomStatus[request.form['status']]
            room.price_per_night = float(request.form['price_per_night'])
            room.capacity = int(request.form['capacity'])
            room.description = request.form['description']
            
            db.session.commit()
            flash('Habitación actualizada correctamente.', 'success')
            return redirect(url_for('rooms.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la habitación: {str(e)}', 'danger')
    
    return render_template('rooms/edit.html', room=room, room_types=RoomType, room_statuses=RoomStatus)

@bp.route('/<int:id>')
@login_required
def view(id):
    room = Room.query.get_or_404(id)
    return render_template('rooms/view.html', room=room)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    room = Room.query.get_or_404(id)
    try:
        db.session.delete(room)
        db.session.commit()
        flash('Habitación eliminada correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la habitación: {str(e)}', 'danger')
    
    return redirect(url_for('rooms.index'))