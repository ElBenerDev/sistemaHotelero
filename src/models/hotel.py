from src.extensions import db
from datetime import datetime

class Hotel(db.Model):
    __tablename__ = 'hotels'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    habitacion = db.Column(db.Integer, nullable=False)
    documento = db.Column(db.String(50), nullable=False)
    fecha_entrada = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_salida = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'habitacion': self.habitacion,
            'documento': self.documento,
            'fecha_entrada': self.fecha_entrada.strftime('%Y-%m-%d %H:%M:%S'),
            'fecha_salida': self.fecha_salida.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_salida else None,
        }