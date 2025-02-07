from src.extensions import db
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    RESERVATION = "Reservación"
    CHECK_IN = "Check-in"
    CHECK_OUT = "Check-out"
    MAINTENANCE = "Mantenimiento"
    CLEANING = "Limpieza"
    SYSTEM = "Sistema"

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(NotificationType), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255))
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('notifications', lazy='dynamic'))

    @property
    def time_ago(self):
        """Retorna el tiempo transcurrido desde la creación de la notificación"""
        now = datetime.utcnow()
        diff = now - self.created_at

        if diff.days > 0:
            return f"hace {diff.days} días"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"hace {hours} horas"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"hace {minutes} minutos"
        else:
            return "hace un momento"

    @classmethod
    def create_for_user(cls, user_id, type_, message, link=None):
        """Crea una notificación para un usuario específico"""
        notification = cls(
            user_id=user_id,
            type=type_,
            message=message,
            link=link
        )
        db.session.add(notification)
        db.session.commit()
        return notification

    @classmethod
    def create_for_all_users(cls, type_, message, link=None):
        """Crea una notificación para todos los usuarios"""
        from src.models.user import User
        notifications = []
        for user in User.query.all():
            notification = cls(
                user_id=user.id,
                type=type_,
                message=message,
                link=link
            )
            notifications.append(notification)
        db.session.add_all(notifications)
        db.session.commit()
        return notifications

    @classmethod
    def notify_new_reservation(cls, reservation):
        """Crea una notificación para una nueva reservación"""
        return cls.create_for_user(
            user_id=reservation.guest.user_id,
            type_=NotificationType.RESERVATION,
            message=f"Nueva reservación para la habitación {reservation.room.number}",
            link=f"/reservations/{reservation.id}"
        )

    @classmethod
    def notify_check_in(cls, reservation):
        """Crea una notificación para un check-in"""
        return cls.create_for_user(
            user_id=reservation.guest.user_id,
            type_=NotificationType.CHECK_IN,
            message=f"Check-in realizado para la habitación {reservation.room.number}",
            link=f"/reservations/{reservation.id}"
        )

    @classmethod
    def notify_check_out(cls, reservation):
        """Crea una notificación para un check-out"""
        return cls.create_for_user(
            user_id=reservation.guest.user_id,
            type_=NotificationType.CHECK_OUT,
            message=f"Check-out realizado para la habitación {reservation.room.number}",
            link=f"/reservations/{reservation.id}"
        )

    def __repr__(self):
        return f'<Notification {self.id}: {self.type.value}>'