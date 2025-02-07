import os
import shutil
from pathlib import Path
import sys

def remove_redundant_files():
    """Elimina archivos redundantes del proyecto"""
    redundant_files = [
        'create_tables.py',
        'migrations.py',
        'manage.py',
        'setup.py',
        'run.py'
    ]
    
    for file in redundant_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✓ Eliminado archivo redundante: {file}")
            except Exception as e:
                print(f"✗ Error eliminando {file}: {e}")

def clean_project():
    """Limpia todos los archivos temporales y generados del proyecto"""
    print("🧹 Iniciando limpieza profunda del proyecto...")

    # Eliminar archivos redundantes
    print("\n🗑️  Eliminando archivos redundantes...")
    remove_redundant_files()

    # Directorios a eliminar
    dirs_to_remove = [
        '__pycache__',
        '.pytest_cache',
        'build',
        'dist',
        '*.egg-info',
        '.mypy_cache',
        'instance'
    ]

    # Extensiones de archivos a eliminar
    file_patterns = [
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '*.so',
        '*.db',
        '*.sqlite',
        '*.sqlite3',
        '*.log',
        '*.pot',
        '*$py.class',
        '*.spec',
        '.DS_Store',
        'Thumbs.db',
        '*.bak',
        '*.swp',
        '*~'
    ]

    root_dir = Path('.')
    removed_dirs = 0
    removed_files = 0

    # Eliminar directorios temporales
    print("\n🗑️  Eliminando directorios temporales...")
    for pattern in dirs_to_remove:
        for path in root_dir.rglob(pattern):
            if path.is_dir() and 'venv' not in str(path):
                try:
                    shutil.rmtree(path)
                    print(f"✓ Eliminado directorio: {path}")
                    removed_dirs += 1
                except Exception as e:
                    print(f"✗ Error eliminando {path}: {e}")

    # Eliminar archivos temporales
    print("\n🗑️  Eliminando archivos temporales...")
    for pattern in file_patterns:
        for path in root_dir.rglob(pattern):
            if path.is_file() and 'venv' not in str(path):
                try:
                    path.unlink()
                    print(f"✓ Eliminado archivo: {path}")
                    removed_files += 1
                except Exception as e:
                    print(f"✗ Error eliminando {path}: {e}")

    print("\n✨ Limpieza completada!")
    print(f"  - Directorios eliminados: {removed_dirs}")
    print(f"  - Archivos eliminados: {removed_files}")

    # Verificar estructura final
    print("\n📁 Estructura final del proyecto:")
    os.system('tree /F /A' if os.name == 'nt' else 'tree -I "venv|__pycache__"')

if __name__ == "__main__":
    try:
        response = input("⚠️  Esta operación eliminará archivos redundantes y temporales. ¿Continuar? [y/N]: ").lower()
        if response == 'y':
            clean_project()
            print("\n✅ Proyecto listo para commit!")
            print("\nPara finalizar la limpieza, ejecuta:")
            print("1. git rm -r --cached .")
            print("2. git add .")
            print("3. git commit -m 'Clean and organize project structure'")
        else:
            print("Operación cancelada.")
    except Exception as e:
        print(f"\n❌ Error durante la limpieza: {e}")
        sys.exit(1)