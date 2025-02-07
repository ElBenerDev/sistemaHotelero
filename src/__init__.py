from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .extensions import db
import os

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = 'tu_clave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensiones
    db.init_app(app)
    migrate = Migrate(app, db)

    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Importar modelos para que Flask-Migrate los detecte
    from .models.notification import Notification, NotificationType
    from .models.user import User
    # Importar otros modelos aquí...

    # Registrar blueprints
    from .routes import auth, rooms, guests, reservations, notifications
    app.register_blueprint(auth.bp)
    app.register_blueprint(rooms.bp)
    app.register_blueprint(guests.bp)
    app.register_blueprint(reservations.bp)
    app.register_blueprint(notifications.bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app