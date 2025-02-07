import PyInstaller.__main__
import os
import shutil

def build_exe():
    """Construir el ejecutable del Sistema Hotelero"""
    print("Iniciando construcción del ejecutable...")
    
    # Limpiar directorio dist si existe
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    
    # Definir archivos y directorios a incluir
    datas = [
        ('src/templates', 'src/templates'),
        ('src/static', 'src/static'),
        ('requirements.txt', '.'),
        ('.flaskenv', '.')
    ]
    
    # Convertir datas a formato de PyInstaller
    datas_str = [f"--add-data={src}{os.pathsep}{dst}" for src, dst in datas]
    
    # Opciones de PyInstaller
    options = [
        'run.py',
        '--onedir',
        '--name=SistemaHotelero',
        '--icon=src/static/img/icon.ico',  # Asegúrate de tener un icono
        '--hidden-import=flask_sqlalchemy',
        '--hidden-import=flask_login',
        '--hidden-import=flask_migrate',
        *datas_str
    ]
    
    try:
        PyInstaller.__main__.run(options)
        print("\nEjecutable creado exitosamente!")
        print("Puedes encontrarlo en: dist/SistemaHotelero/SistemaHotelero.exe")
        return True
    except Exception as e:
        print(f"Error creando el ejecutable: {str(e)}")
        return False

if __name__ == "__main__":
    build_exe()