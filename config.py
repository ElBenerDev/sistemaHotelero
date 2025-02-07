import os
from datetime import timedelta

class Config:
    # Obtener la ruta del directorio del usuario
    USER_HOME = os.path.expanduser('~')
    
    # Crear un directorio para la aplicación
    APP_DIR = os.path.join(USER_HOME, 'SistemaHotelero')
    
    # Directorio para logs
    LOG_DIR = os.path.join(APP_DIR, 'logs')
    
    # Directorio para la base de datos
    DB_DIR = os.path.join(APP_DIR, 'data')
    
    # Crear directorios si no existen
    for directory in [APP_DIR, LOG_DIR, DB_DIR]:
        os.makedirs(directory, exist_ok=True)
    
    # Configuración básica
    SECRET_KEY = 'dev'
    
    # Ruta de la base de datos local
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(DB_DIR, "hotel.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de la sesión
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)