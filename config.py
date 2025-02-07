import os

class Config:
    # Configuración básica
    SECRET_KEY = 'tu_clave_secreta_aqui'
    
    # Configuración de la base de datos
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'hotel.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False