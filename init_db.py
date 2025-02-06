from src import create_app, db
from src.models.user import User
from werkzeug.security import generate_password_hash

def init_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        # Crear usuario de prueba
        if not User.query.filter_by(username='admin').first():
            user = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(user)
            db.session.commit()
            
        print("¡Base de datos inicializada correctamente!")

if __name__ == "__main__":
    init_database()