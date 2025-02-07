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

def setup_logging():
    """Configurar el sistema de logs"""
    from config import Config
    
    # Asegurarse de que el directorio de logs existe
    os.makedirs(Config.LOG_DIR, exist_ok=True)
    
    log_file = os.path.join(Config.LOG_DIR, 'sistema.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Añadir logging a consola también
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    
    return logging.getLogger('setup')

def init_notifications(logger, app, admin_user):
    """Inicializar las notificaciones del sistema"""
    try:
        with app.app_context():
            logger.info("Verificando notificaciones iniciales...")
            
            # Verificar si ya existen notificaciones
            if Notification.query.count() == 0:
                logger.info("Creando notificaciones iniciales...")
                current_time = datetime.utcnow()
                
                notifications = [
                    Notification(
                        user_id=admin_user.id,
                        type=NotificationType.SYSTEM,
                        message="¡Bienvenido al Sistema Hotelero!",
                        link="/dashboard",
                        created_at=current_time
                    ),
                    Notification(
                        user_id=admin_user.id,
                        type=NotificationType.SYSTEM,
                        message="Sistema de notificaciones activado",
                        link="/notifications",
                        created_at=current_time
                    ),
                    Notification(
                        user_id=admin_user.id,
                        type=NotificationType.MAINTENANCE,
                        message="Configuración inicial completada",
                        link="/settings",
                        created_at=current_time
                    )
                ]
                
                db.session.add_all(notifications)
                db.session.commit()
                logger.info("Notificaciones iniciales creadas exitosamente")
            else:
                logger.info("Las notificaciones ya están inicializadas")
            
            return True
            
    except Exception as e:
        logger.error(f"Error inicializando notificaciones: {str(e)}")
        logger.error("Traceback completo:")
        logger.error(traceback.format_exc())
        return False

def init_database(logger):
    """Inicializar la base de datos"""
    try:
        logger.info("Creando aplicación...")
        app = create_app()
        
        logger.info("Verificando directorio de la base de datos...")
        from config import Config
        db_dir = os.path.dirname(Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', ''))
        os.makedirs(db_dir, exist_ok=True)
        
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
            logger.info("Inicializando sistema de notificaciones...")
            if not init_notifications(logger, app, admin):
                logger.error("Error inicializando notificaciones")
                return False
            
            logger.info("Base de datos inicializada correctamente")
            return True
    except Exception as e:
        logger.error(f"Error inicializando la base de datos: {str(e)}")
        logger.error("Traceback completo:")
        logger.error(traceback.format_exc())
        return False

def check_dependencies():
    """Verificar que todas las dependencias estén instaladas"""
    required = [
        'flask',
        'flask-sqlalchemy',
        'flask-login',
        'werkzeug',
        'click',
        'jinja2',
        'itsdangerous',
        'flask-migrate'
        # python-dotenv removido de la lista ya que está instalado
    ]
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    return missing

def verify_directories():
    """Verificar y crear directorios necesarios"""
    try:
        from config import Config
        
        # Lista de directorios a verificar
        directories = [
            Config.APP_DIR,
            Config.LOG_DIR,
            os.path.dirname(Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', ''))
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Directorio creado: {directory}")
            else:
                print(f"Directorio existente: {directory}")
                
        return True
    except Exception as e:
        print(f"Error verificando directorios: {str(e)}")
        return False

def main():
    """Función principal de configuración"""
    print("Iniciando configuración del sistema...")
    
    # Verificar directorios
    print("\nVerificando directorios...")
    if not verify_directories():
        print("Error: No se pudieron crear los directorios necesarios")
        return False
    
    # Configurar logging
    print("\nConfigurando sistema de logs...")
    logger = setup_logging()
    
    # Verificar dependencias
    print("\nVerificando dependencias...")
    missing_deps = check_dependencies()
    if missing_deps:
        logger.error(f"Faltan dependencias: {', '.join(missing_deps)}")
        print(f"Error: Faltan las siguientes dependencias: {', '.join(missing_deps)}")
        print("Por favor, ejecute: pip install " + " ".join(missing_deps))
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