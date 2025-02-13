import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self):
        self.db_file = "hotel_database.db"
        self.connection = None
        self.create_connection()
        self.create_tables()

    def create_connection(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            print("Conexión a SQLite establecida")
        except Error as e:
            print(f"Error al conectar a SQLite: {e}")

    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            
            # Tabla para huéspedes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS huespedes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    documento TEXT NOT NULL,
                    habitacion INTEGER NOT NULL,
                    fecha_entrada TEXT NOT NULL,
                    fecha_salida TEXT
                )
            ''')
            
            # Tabla para habitaciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS habitaciones (
                    numero INTEGER PRIMARY KEY,
                    tipo TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    precio REAL NOT NULL
                )
            ''')
            
            self.connection.commit()
            
        except Error as e:
            print(f"Error al crear las tablas: {e}")

    def guardar_huesped(self, nombre, documento, habitacion, fecha_entrada):
        sql = '''INSERT INTO huespedes(nombre, documento, habitacion, fecha_entrada)
                VALUES(?,?,?,?)'''
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (nombre, documento, habitacion, fecha_entrada))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error al guardar huésped: {e}")
            return False

    def obtener_huespedes(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM huespedes")
            return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener huéspedes: {e}")
            return []

    def cerrar_conexion(self):
        if self.connection:
            self.connection.close()