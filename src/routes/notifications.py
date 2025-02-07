from flask import Blueprint, jsonify, redirect, url_for, render_template
from flask_login import login_required, current_user
from src.models.notification import Notification
from src.extensions import db

bp = Blueprint('notifications', __name__, url_prefix='/notifications')

@bp.route('/')
@login_required
def index():
    notifications = current_user.notifications.order_by(Notification.created_at.desc()).all()
    return render_template('notifications/index.html', notifications=notifications)

@bp.route('/unread')
@login_required
def get_unread():
    """Retorna el número de notificaciones no leídas y las últimas 5"""
    unread_notifications = current_user.notifications.filter_by(is_read=False).order_by(Notification.created_at.desc()).limit(5).all()
    count = current_user.notifications.filter_by(is_read=False).count()
    
    return jsonify({
        'count': count,
        'notifications': [{
            'id': n.id,
            'type': n.type.value,
            'message': n.message,
            'link': n.link,
            'time_ago': n.time_ago
        } for n in unread_notifications]
    })

@bp.route('/<int:id>/read', methods=['POST'])
@login_required
def mark_as_read(id):
    """Marca una notificación como leída"""
    notification = Notification.query.get_or_404(id)
    if notification.user_id == current_user.id:
        notification.is_read = True
        db.session.commit()
    return jsonify({'success': True})

@bp.route('/read-all', methods=['POST'])
@login_required
def mark_all_as_read():
    """Marca todas las notificaciones como leídas"""
    current_user.notifications.filter_by(is_read=False).update({Notification.is_read: True})
    db.session.commit()
    return jsonify({'success': True})