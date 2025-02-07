from src import create_app
from src.extensions import db
from src.models.notification import Notification, NotificationType
from src.models.user import User
from datetime import datetime

app = create_app()

def init_db():
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("Tablas creadas exitosamente")
        
        # Crear notificaciones de prueba
        user = User.query.filter_by(username='admin').first()
        if user:
            # Verificar si ya existen notificaciones
            existing_notifications = Notification.query.count()
            if existing_notifications == 0:
                current_time = datetime.utcnow()
                notifications = [
                    Notification(
                        user_id=user.id,
                        type=NotificationType.SYSTEM,
                        message="Bienvenido al Sistema Hotelero",
                        link="/dashboard",
                        created_at=current_time
                    ),
                    Notification(
                        user_id=user.id,
                        type=NotificationType.MAINTENANCE,
                        message="Bienvenido al módulo de notificaciones",
                        link="/maintenance",
                        created_at=current_time
                    ),
                    Notification(
                        user_id=user.id,
                        type=NotificationType.CLEANING,
                        message="Las notificaciones te ayudarán a estar al tanto de todo",
                        link="/rooms/101",
                        created_at=current_time
                    )
                ]
                
                try:
                    db.session.add_all(notifications)
                    db.session.commit()
                    print("Notificaciones creadas exitosamente")
                except Exception as e:
                    print(f"Error al crear notificaciones: {str(e)}")
                    db.session.rollback()
            else:
                print(f"Ya existen {existing_notifications} notificaciones en la base de datos")
        else:
            print("Usuario 'admin' no encontrado")

if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")