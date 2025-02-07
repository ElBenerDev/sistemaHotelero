import os
import sys
import sqlite3
from src import create_app
from src.extensions import db
from src.models.user import User
from src.models.notification import Notification, NotificationType
from werkzeug.security import generate_password_hash
import logging
import traceback
from datetime import datetime

APP_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(APP_DIR, 'instance')
LOG_DIR = os.path.join(APP_DIR, 'logs')

def setup_logging():
    """Configurar el sistema de logs"""
    os.makedirs(LOG_DIR, exist_ok=True)
    
    log_file = os.path.join(LOG_DIR, 'sistema.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    
    return logging.getLogger('setup')

def verify_dependencies():
    """Verificar y instalar dependencias necesarias"""
    try:
        import pkg_resources
        import subprocess

        with open('requirements.txt') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
        missing = []

        for requirement in requirements:
            package = requirement.split('==')[0]
            if package.lower() not in installed:
                missing.append(requirement)

        if missing:
            print("Instalando dependencias faltantes...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
            print("Dependencias instaladas correctamente")
        
        return True
    except Exception as e:
        print(f"Error verificando dependencias: {str(e)}")
        return False

def init_database(logger):
    """Inicializar la base de datos"""
    try:
        logger.info("Creando aplicación...")
        app = create_app()
        
        logger.info("Verificando directorio de la base de datos...")
        os.makedirs(DB_DIR, exist_ok=True)
        
        logger.info("Inicializando contexto de la aplicación...")
        with app.app_context():
            logger.info("Creando todas las tablas...")
            db.create_all()
            
            logger.info("Verificando usuario administrador...")
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@sistema.local',
                    password_hash=generate_password_hash('admin123')
                )
                db.session.add(admin)
                db.session.commit()
                logger.info("Usuario administrador creado exitosamente")
            
            # Inicializar notificaciones
            if Notification.query.count() == 0:
                logger.info("Creando notificaciones iniciales...")
                notifications = [
                    Notification(
                        user_id=admin.id,
                        type=NotificationType.SYSTEM,
                        message="¡Bienvenido al Sistema Hotelero!",
                        link="/dashboard"
                    ),
                    Notification(
                        user_id=admin.id,
                        type=NotificationType.SYSTEM,
                        message="Sistema inicializado correctamente",
                        link="/notifications"
                    )
                ]
                db.session.add_all(notifications)
                db.session.commit()
                logger.info("Notificaciones iniciales creadas")
            
            return True
    except Exception as e:
        logger.error(f"Error inicializando la base de datos: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def create_directories():
    """Crear directorios necesarios"""
    directories = [
        DB_DIR,
        LOG_DIR,
        os.path.join(APP_DIR, 'src', 'static', 'uploads'),
        os.path.join(APP_DIR, 'src', 'static', 'temp')
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Directorio creado/verificado: {directory}")
        except Exception as e:
            print(f"Error creando directorio {directory}: {str(e)}")
            return False
    return True

def main():
    """Función principal de configuración"""
    print("Iniciando configuración del Sistema Hotelero...")
    
    # Crear directorios necesarios
    print("\nCreando directorios necesarios...")
    if not create_directories():
        print("Error: No se pudieron crear los directorios necesarios")
        return False
    
    # Configurar logging
    print("\nConfigurando sistema de logs...")
    logger = setup_logging()
    
    # Verificar dependencias
    print("\nVerificando dependencias...")
    if not verify_dependencies():
        logger.error("Error verificando dependencias")
        return False
    
    # Inicializar base de datos
    print("\nInicializando base de datos...")
    if not init_database(logger):
        print("Error: No se pudo inicializar la base de datos")
        return False
    
    print("\n¡Sistema configurado exitosamente!")
    print("\nCredenciales de administrador:")
    print("Usuario: admin")
    print("Contraseña: admin123")
    
    logger.info("Configuración completada exitosamente")
    return True

if __name__ == "__main__":
    sys.exit(0 if main() else 1)