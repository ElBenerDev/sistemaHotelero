from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from src.models.room import Room, RoomType, RoomStatus
from src.forms.room import RoomForm
from src import db

bp = Blueprint('rooms', __name__, url_prefix='/rooms')

@bp.route('/')
@login_required
def index():
    # Obtener el filtro de estado si existe
    status_filter = request.args.get('status')
    type_filter = request.args.get('type')
    floor_filter = request.args.get('floor')
    
    # Crear la consulta base
    query = Room.query
    
    # Aplicar filtros si existen
    if status_filter:
        query = query.filter_by(status=RoomStatus[status_filter])
    if type_filter:
        query = query.filter_by(type=RoomType[type_filter])
    if floor_filter:
        query = query.filter_by(floor=floor_filter)
    
    # Ordenar por número de habitación
    rooms = query.order_by(Room.number).all()
    
    # Obtener valores únicos para los filtros
    floors = sorted(set(room.floor for room in Room.query.all()))
    
    return render_template('rooms/index.html', 
                         rooms=rooms,
                         room_types=RoomType,
                         room_statuses=RoomStatus,
                         floors=floors,
                         current_status=status_filter,
                         current_type=type_filter,
                         current_floor=floor_filter)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = RoomForm()
    if form.validate_on_submit():
        room = Room(
            number=form.number.data,
            type=RoomType[form.type.data],
            status=RoomStatus[form.status.data],
            price=form.price.data,
            capacity=form.capacity.data,
            description=form.description.data,
            floor=form.floor.data
        )
        try:
            db.session.add(room)
            db.session.commit()
            flash('Habitación creada exitosamente.', 'success')
            return redirect(url_for('rooms.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la habitación. El número puede estar duplicado.', 'danger')
    return render_template('rooms/add.html', form=form)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    room = Room.query.get_or_404(id)
    # Para GET request, pre-poblar el formulario con los valores actuales
    if request.method == 'GET':
        form = RoomForm()
        form.number.data = room.number
        form.type.data = room.type.name
        form.status.data = room.status.name
        form.price.data = room.price
        form.capacity.data = room.capacity
        form.description.data = room.description
        form.floor.data = room.floor
    else:
        form = RoomForm()
    
    if form.validate_on_submit():
        try:
            room.number = form.number.data
            room.type = RoomType[form.type.data]
            room.status = RoomStatus[form.status.data]
            room.price = form.price.data
            room.capacity = form.capacity.data
            room.description = form.description.data
            room.floor = form.floor.data
            
            db.session.commit()
            flash('Habitación actualizada exitosamente.', 'success')
            return redirect(url_for('rooms.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar la habitación.', 'danger')
    
    return render_template('rooms/edit.html', form=form, room=room)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    room = Room.query.get_or_404(id)
    try:
        db.session.delete(room)
        db.session.commit()
        flash('Habitación eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar la habitación. Puede que tenga reservaciones asociadas.', 'danger')
    return redirect(url_for('rooms.index'))