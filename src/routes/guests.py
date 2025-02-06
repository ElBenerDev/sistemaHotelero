from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('guests', __name__, url_prefix='/guests')

@bp.route('/')
@login_required
def index():
    guests = [
        {
            'id': '001',
            'name': 'Juan Pérez',
            'email': 'juan@example.com',
            'phone': '123-456-7890',
            'status': 'Check-in'
        },
        {
            'id': '002',
            'name': 'María García',
            'email': 'maria@example.com',
            'phone': '098-765-4321',
            'status': 'Reserved'
        }
        # Aquí puedes agregar más huéspedes de ejemplo
    ]
    return render_template('guests/index.html', guests=guests)