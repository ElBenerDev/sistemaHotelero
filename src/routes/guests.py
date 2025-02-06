from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from src.models.guest import Guest
from src.extensions import db
from datetime import datetime

bp = Blueprint('guests', __name__, url_prefix='/guests')

@bp.route('/')
@login_required
def index():
    # Obtener parámetros de búsqueda y ordenamiento
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Construir query base
    query = Guest.query

    # Aplicar búsqueda si existe
    if search:
        query = query.filter(
            (Guest.first_name.ilike(f'%{search}%')) |
            (Guest.last_name.ilike(f'%{search}%')) |
            (Guest.email.ilike(f'%{search}%')) |
            (Guest.phone.ilike(f'%{search}%'))
        )

    # Aplicar ordenamiento
    if sort_by and order:
        sort_column = getattr(Guest, sort_by)
        if order == 'desc':
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)

    # Paginar resultados
    guests = query.paginate(page=page, per_page=per_page)
    return render_template('guests/index.html', guests=guests, search=search)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        try:
            guest = Guest(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                email=request.form['email'],
                phone=request.form['phone'],
                address=request.form['address'],
                city=request.form['city'],
                country=request.form['country'],
                identification_type=request.form['identification_type'],
                identification_number=request.form['identification_number']
            )
            db.session.add(guest)
            db.session.commit()
            flash('Huésped agregado correctamente.', 'success')
            return redirect(url_for('guests.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar el huésped: {str(e)}', 'danger')
            return redirect(url_for('guests.add'))

    return render_template('guests/add.html')

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    guest = Guest.query.get_or_404(id)
    if request.method == 'POST':
        try:
            guest.first_name = request.form['first_name']
            guest.last_name = request.form['last_name']
            guest.email = request.form['email']
            guest.phone = request.form['phone']
            guest.address = request.form['address']
            guest.city = request.form['city']
            guest.country = request.form['country']
            guest.identification_type = request.form['identification_type']
            guest.identification_number = request.form['identification_number']
            guest.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('Huésped actualizado correctamente.', 'success')
            return redirect(url_for('guests.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el huésped: {str(e)}', 'danger')
    
    return render_template('guests/edit.html', guest=guest)

@bp.route('/<int:id>')
@login_required
def view(id):
    guest = Guest.query.get_or_404(id)
    return render_template('guests/view.html', guest=guest)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    guest = Guest.query.get_or_404(id)
    try:
        db.session.delete(guest)
        db.session.commit()
        flash('Huésped eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el huésped: {str(e)}', 'danger')
    
    return redirect(url_for('guests.index'))