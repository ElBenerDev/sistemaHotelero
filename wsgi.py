from src import create_app
from src.extensions import db
from src.models.user import User
from werkzeug.security import generate_password_hash
import os

app = create_app()

def init_db():
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        # Crear usuario admin si no existe
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@sistema.local',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()
            print("Usuario admin creado exitosamente")

if __name__ == '__main__':
    # Asegurarse de que estamos en el directorio correcto
    app_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(app_dir)
    
    # Inicializar la base de datos
    init_db()
    
    # Ejecutar la aplicación
    app.run(debug=True)