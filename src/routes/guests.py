from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required
from src.models.guest import Guest, DocumentType
from src.extensions import db
from datetime import datetime

bp = Blueprint('guests', __name__, url_prefix='/guests')

@bp.route('/')
@login_required
def index():
    guests = Guest.query.order_by(Guest.first_name, Guest.last_name).all()
    return render_template('guests/index.html', guests=guests)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        try:
            # Solo nombre, apellido y teléfono son requeridos
            guest = Guest(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                phone=request.form['phone'],
                # Campos opcionales
                id_type=request.form.get('id_type'),  # Usando .get() para campos opcionales
                id_number=request.form.get('id_number'),
                email=request.form.get('email'),
                address=request.form.get('address')
            )
            
            db.session.add(guest)
            db.session.commit()
            
            flash('Huésped registrado exitosamente', 'success')
            return redirect(url_for('guests.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el huésped: {str(e)}', 'danger')
    
    return render_template('guests/new.html', document_types=DocumentType)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    guest = Guest.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Solo nombre, apellido y teléfono son requeridos
            guest.first_name = request.form['first_name']
            guest.last_name = request.form['last_name']
            guest.phone = request.form['phone']
            # Campos opcionales
            guest.id_type = request.form.get('id_type')
            guest.id_number = request.form.get('id_number')
            guest.email = request.form.get('email')
            guest.address = request.form.get('address')
            guest.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('Huésped actualizado exitosamente', 'success')
            return redirect(url_for('guests.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el huésped: {str(e)}', 'danger')
    
    return render_template('guests/edit.html', guest=guest, document_types=DocumentType)

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
        flash('Huésped eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el huésped: {str(e)}', 'danger')
    
    return redirect(url_for('guests.index'))

@bp.route('/search')
@login_required
def search():
    term = request.args.get('term', '')
    guests = Guest.query.filter(
        (Guest.first_name.ilike(f'%{term}%')) |
        (Guest.last_name.ilike(f'%{term}%')) |
        (Guest.id_number.ilike(f'%{term}%'))
    ).limit(10).all()
    
    return jsonify([{
        'id': guest.id,
        'text': f'{guest.full_name} - {guest.id_type.value}: {guest.id_number}'
    } for guest in guests])