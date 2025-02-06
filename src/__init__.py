from flask import Flask
from config import Config
from src.extensions import db, login_manager
from src.routes import reservations
from src.routes import reports

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones con la aplicación
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        # Importar modelos
        from src.models.user import User
        from src.models.room import Room
        from src.models.guest import Guest
        from src.models.reservation import Reservation

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # Importar y registrar blueprints
        from src.routes import main, auth, rooms, guests, reservations, calendar, reports
        app.register_blueprint(main.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(rooms.bp)
        app.register_blueprint(guests.bp)
        app.register_blueprint(reservations.bp)
        app.register_blueprint(calendar.bp)
        app.register_blueprint(reports.bp)  # Agregada esta línea

        # Crear todas las tablas
        db.create_all()

    return app