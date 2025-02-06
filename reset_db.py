import os
from src import create_app
from src.extensions import db
from src.models.user import User
from src.models.room import Room, RoomType, RoomStatus
from src.models.guest import Guest
from src.models.reservation import Reservation, ReservationStatus
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def reset_database():
    app = create_app()
    
    with app.app_context():
        # Asegurarse de que la carpeta src existe
        if not os.path.exists('src'):
            os.makedirs('src')
            
        # Eliminar la base de datos si existe
        db_path = os.path.join('src', 'hotel_management.db')
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Base de datos anterior eliminada: {db_path}")
            
        # Crear todas las tablas
        db.create_all()
        print("Tablas creadas correctamente")
        
        # Crear usuario administrador
        admin = User(
            username='admin',
            email='admin@example.com'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Crear habitaciones por defecto
        default_rooms = [
            Room(number='101', type=RoomType.SINGLE, status=RoomStatus.AVAILABLE, price=100.00, capacity=1, floor=1, description='Habitación individual con vista a la ciudad'),
            Room(number='102', type=RoomType.DOUBLE, status=RoomStatus.AVAILABLE, price=150.00, capacity=2, floor=1, description='Habitación doble con balcón'),
            Room(number='103', type=RoomType.SINGLE, status=RoomStatus.AVAILABLE, price=100.00, capacity=1, floor=1),
            Room(number='104', type=RoomType.DOUBLE, status=RoomStatus.AVAILABLE, price=150.00, capacity=2, floor=1),
            Room(number='201', type=RoomType.SUITE, status=RoomStatus.AVAILABLE, price=250.00, capacity=2, floor=2, description='Suite de lujo con sala de estar'),
            Room(number='202', type=RoomType.FAMILY, status=RoomStatus.AVAILABLE, price=200.00, capacity=4, floor=2, description='Habitación familiar espaciosa'),
            Room(number='203', type=RoomType.SINGLE, status=RoomStatus.AVAILABLE, price=100.00, capacity=1, floor=2),
            Room(number='204', type=RoomType.DOUBLE, status=RoomStatus.AVAILABLE, price=150.00, capacity=2, floor=2),
            Room(number='301', type=RoomType.SINGLE, status=RoomStatus.AVAILABLE, price=100.00, capacity=1, floor=3),
            Room(number='302', type=RoomType.DOUBLE, status=RoomStatus.AVAILABLE, price=150.00, capacity=2, floor=3),
            Room(number='303', type=RoomType.SUITE, status=RoomStatus.AVAILABLE, price=250.00, capacity=2, floor=3),
            Room(number='304', type=RoomType.FAMILY, status=RoomStatus.AVAILABLE, price=200.00, capacity=4, floor=3),
            Room(number='401', type=RoomType.SINGLE, status=RoomStatus.AVAILABLE, price=100.00, capacity=1, floor=4),
            Room(number='402', type=RoomType.DOUBLE, status=RoomStatus.AVAILABLE, price=150.00, capacity=2, floor=4),
            Room(number='403', type=RoomType.SUITE, status=RoomStatus.AVAILABLE, price=250.00, capacity=2, floor=4),
        ]
        
        for room in default_rooms:
            db.session.add(room)

        # Crear algunos huéspedes de ejemplo
        guests = [
            Guest(
                first_name='Juan',
                last_name='Pérez',
                email='juan.perez@example.com',
                phone='555-0101',
                document_type='DNI',
                document_number='12345678'
            ),
            Guest(
                first_name='María',
                last_name='García',
                email='maria.garcia@example.com',
                phone='555-0102',
                document_type='DNI',
                document_number='87654321'
            ),
            Guest(
                first_name='Carlos',
                last_name='López',
                email='carlos.lopez@example.com',
                phone='555-0103',
                document_type='DNI',
                document_number='11223344'
            ),
        ]

        for guest in guests:
            db.session.add(guest)

        # Hacer commit para tener los IDs de habitaciones y huéspedes
        db.session.commit()

        # Crear algunas reservaciones de ejemplo
        now = datetime.utcnow()
        reservations = [
            # Reservación activa (checked-in)
            Reservation(
                guest_id=1,
                room_id=1,
                check_in=now - timedelta(days=1),
                check_out=now + timedelta(days=2),
                status=ReservationStatus.CHECKED_IN,
                total_price=300.00,
                notes='Cliente VIP'
            ),
            # Reservación futura (confirmada)
            Reservation(
                guest_id=2,
                room_id=2,
                check_in=now + timedelta(days=5),
                check_out=now + timedelta(days=8),
                status=ReservationStatus.CONFIRMED,
                total_price=450.00
            ),
            # Reservación pasada (checked-out)
            Reservation(
                guest_id=3,
                room_id=3,
                check_in=now - timedelta(days=10),
                check_out=now - timedelta(days=8),
                status=ReservationStatus.CHECKED_OUT,
                total_price=200.00
            ),
            # Más reservaciones activas
            Reservation(
                guest_id=1,
                room_id=4,
                check_in=now - timedelta(days=2),
                check_out=now + timedelta(days=3),
                status=ReservationStatus.CHECKED_IN,
                total_price=450.00
            ),
            Reservation(
                guest_id=2,
                room_id=5,
                check_in=now - timedelta(days=1),
                check_out=now + timedelta(days=4),
                status=ReservationStatus.CHECKED_IN,
                total_price=750.00
            ),
            # Algunas reservaciones pendientes
            Reservation(
                guest_id=3,
                room_id=6,
                check_in=now + timedelta(days=1),
                check_out=now + timedelta(days=5),
                status=ReservationStatus.PENDING,
                total_price=800.00
            ),
            Reservation(
                guest_id=1,
                room_id=7,
                check_in=now + timedelta(days=7),
                check_out=now + timedelta(days=10),
                status=ReservationStatus.PENDING,
                total_price=300.00
            ),
        ]

        for reservation in reservations:
            db.session.add(reservation)
            # Actualizar el estado de la habitación si está ocupada
            if reservation.status == ReservationStatus.CHECKED_IN:
                room = Room.query.get(reservation.room_id)
                room.status = RoomStatus.OCCUPIED

        db.session.commit()

        print("Base de datos inicializada con:")
        print(f"- {len(default_rooms)} habitaciones")
        print(f"- {len(guests)} huéspedes")
        print(f"- {len(reservations)} reservaciones")
        print("\nUsuario administrador creado:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\n¡Base de datos inicializada correctamente!")

if __name__ == "__main__":
    reset_database()