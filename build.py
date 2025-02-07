import PyInstaller.__main__
import os
import shutil
import sqlite3

def create_directory_structure(base_dir):
    """Crear estructura de directorios necesaria"""
    directories = [
        os.path.join(base_dir, 'src'),
        os.path.join(base_dir, 'src', 'static'),
        os.path.join(base_dir, 'src', 'templates'),
        os.path.join(base_dir, 'instance'),  # Directorio para la base de datos
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Creado directorio: {directory}")

def main():
    print("Iniciando construcción del ejecutable...")
    
    # Limpiar dist anterior
    if os.path.exists('dist'):
        shutil.rmtree('dist')
        print("Carpeta dist anterior eliminada")

    # Crear el ejecutable
    args = [
        'wsgi.py',
        '--name=SistemaHotelero',
        '--onefile',
        '--clean',
        '--add-data', f'src/templates{os.pathsep}src/templates',
        '--add-data', f'src/static{os.pathsep}src/static',
        '--add-data', f'.flaskenv{os.pathsep}.',
        '--add-data', f'config.py{os.pathsep}.',
        '--hidden-import', 'flask',
        '--hidden-import', 'flask_sqlalchemy',
        '--hidden-import', 'flask_login',
        '--hidden-import', 'flask_migrate',
        '--hidden-import', 'sqlalchemy',
        '--hidden-import', 'src.models.user',
        '--hidden-import', 'src.models.guest',
        '--hidden-import', 'src.models.room',
        '--hidden-import', 'src.models.reservation',
        '--hidden-import', 'src.models.notification'
    ]

    try:
        PyInstaller.__main__.run(args)
        print("\nEjecutable creado exitosamente")
        
        # Crear estructura de directorios en dist
        dist_dir = os.path.join('dist', 'SistemaHotelero')
        create_directory_structure(dist_dir)
        
        # Copiar archivos necesarios
        files_to_copy = [
            ('.flaskenv', os.path.join(dist_dir, '.flaskenv')),
            ('config.py', os.path.join(dist_dir, 'config.py'))
        ]
        
        for src, dst in files_to_copy:
            if os.path.exists(src):
                shutil.copy2(src, dst)
                print(f"Copiado: {src} -> {dst}")
            else:
                print(f"Advertencia: Archivo no encontrado: {src}")
        
        print("\nConstrucción completada exitosamente")
        print(f"El ejecutable se encuentra en: {os.path.abspath(os.path.join('dist', 'SistemaHotelero', 'SistemaHotelero.exe'))}")
        return True
        
    except Exception as e:
        print(f"Error durante la construcción: {str(e)}")
        return False

if __name__ == "__main__":
    main()