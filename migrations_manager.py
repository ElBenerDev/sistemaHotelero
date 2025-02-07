from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.update(
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'hotel.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    MIGRATION_DIR=os.path.join(basedir, 'migrations')
)

# Inicializar extensiones
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importar modelos
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

# Importar el resto de los modelos
from src.models.room import Room, RoomType, RoomStatus
from src.models.guest import Guest
from src.models.reservation import Reservation, ReservationStatus

if __name__ == '__main__':
    app.run()