import os
import logging
from src import create_app
from config import Config

def setup_logging():
    """Configurar el sistema de logs"""
    log_file = os.path.join(Config.LOG_DIR, 'sistema.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Añadir logging a consola
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    
    return logging.getLogger('sistema')

def main():
    """Función principal para ejecutar la aplicación"""
    logger = setup_logging()
    logger.info("Iniciando Sistema Hotelero...")
    
    try:
        app = create_app()
        logger.info("Servidor iniciado en http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logger.error(f"Error al ejecutar la aplicación: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    main()