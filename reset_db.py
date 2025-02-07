from src import create_app, db
from src.models import User, Guest, Room, Reservation
from src.models.room import RoomType, RoomStatus
from werkzeug.security import generate_password_hash

def reset_database():
    app = create_app()
    with app.app_context():
        print("Eliminando base de datos existente...")
        db.drop_all()
        print("Creando nueva base de datos...")
        db.create_all()
        
        # Crear usuario admin por defecto
        admin_user = User(
            username='admin',
            password_hash=generate_password_hash('admin'),
            is_admin=True
        )
        db.session.add(admin_user)
        
        # Crear usuario regular de ejemplo
        regular_user = User(
            username='usuario',
            password_hash=generate_password_hash('usuario'),
            is_admin=False
        )
        db.session.add(regular_user)
        
        # Crear algunas habitaciones por defecto
        default_rooms = [
            Room(
                number='101',
                floor=1,
                type=RoomType.SINGLE,
                status=RoomStatus.AVAILABLE,
                price_per_night=100.0,
                capacity=1,
                description='Habitación individual estándar'
            ),
            Room(
                number='102',
                floor=1,
                type=RoomType.DOUBLE,
                status=RoomStatus.AVAILABLE,
                price_per_night=150.0,
                capacity=2,
                description='Habitación doble con vista a la ciudad'
            ),
            Room(
                number='201',
                floor=2,
                type=RoomType.SUITE,
                status=RoomStatus.AVAILABLE,
                price_per_night=300.0,
                capacity=2,
                description='Suite de lujo con balcón'
            ),
            Room(
                number='301',
                floor=3,
                type=RoomType.FAMILY,
                status=RoomStatus.AVAILABLE,
                price_per_night=250.0,
                capacity=4,
                description='Habitación familiar con dos camas dobles'
            ),
        ]
        
        for room in default_rooms:
            db.session.add(room)

        try:
            db.session.commit()
            print("¡Base de datos recreada exitosamente!")
            print("\nUsuarios creados:")
            print("1. Admin")
            print("   - Username: admin")
            print("   - Password: admin")
            print("\n2. Usuario Regular")
            print("   - Username: usuario")
            print("   - Password: usuario")
            print("\nHabitaciones de muestra creadas:")
            for room in default_rooms:
                print(f"- Habitación {room.number} (Piso {room.floor}): {room.type.value} (${room.price_per_night}/noche)")
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear datos iniciales: {str(e)}")

if __name__ == "__main__":
    reset_database()