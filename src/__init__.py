from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .extensions import db
import os
import sys

def create_app():
    app = Flask(__name__)
    
    # Configuración básica
    app.config['SECRET_KEY'] = 'tu_clave_secreta'
    
    # Determinar si estamos en un ejecutable o en desarrollo
    if getattr(sys, 'frozen', False):
        # Si es un ejecutable, usar el directorio instance junto al exe
        application_path = os.path.dirname(sys.executable)
        instance_path = os.path.join(application_path, 'instance')
    else:
        # Si es desarrollo, usar el directorio actual
        application_path = os.path.dirname(os.path.abspath(__file__))
        instance_path = os.path.join(os.path.dirname(application_path), 'instance')
    
    # Asegurar que el directorio instance existe
    os.makedirs(instance_path, exist_ok=True)
    
    # Configurar la ruta de la base de datos
    db_path = os.path.join(instance_path, 'hotel.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # Inicializar extensiones
    db.init_app(app)
    migrate = Migrate(app, db)

    # Configurar Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Importar modelos
    from .models.user import User
    from .models.guest import Guest
    from .models.room import Room
    from .models.reservation import Reservation
    from .models.notification import Notification
    from .models.hotel import Hotel

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar blueprints
    from .routes.auth import bp as auth_bp
    from .routes.main import bp as main_bp
    from .routes.rooms import bp as rooms_bp
    from .routes.guests import bp as guests_bp
    from .routes.reservations import bp as reservations_bp
    from .routes.notifications import bp as notifications_bp
    from .routes.calendar import bp as calendar_bp
    from .routes.reports import bp as reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(guests_bp)
    app.register_blueprint(reservations_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(calendar_bp)
    app.register_blueprint(reports_bp)

    return app