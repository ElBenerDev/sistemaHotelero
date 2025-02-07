import os
import shutil
from pathlib import Path
import sys

def clean_project():
    """Limpia todos los archivos temporales y generados del proyecto"""
    print("🧹 Iniciando limpieza profunda del proyecto...")

    # Primero, eliminar todo el contenido de venv si existe
    venv_path = Path('venv')
    if venv_path.exists():
        choice = input("⚠️  ¿Deseas eliminar completamente el entorno virtual (venv)? [y/N]: ").lower()
        if choice == 'y':
            try:
                shutil.rmtree(venv_path)
                print("✓ Entorno virtual eliminado completamente")
            except Exception as e:
                print(f"✗ Error eliminando venv: {e}")
        else:
            print("Manteniendo el entorno virtual...")

    # Directorios a eliminar completamente
    dirs_to_remove = [
        '__pycache__',
        '.pytest_cache',
        '.coverage',
        'build',
        'dist',
        '.eggs',
        '*.egg-info',
        '.tox',
        '.mypy_cache',
        '.dmypy.json',
        '.pyre',
        'instance',
        'logs'
    ]

    # Extensiones de archivos a eliminar
    file_patterns = [
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '*.so',
        '*.dylib',
        '*.dll',
        '*.db',
        '*.sqlite',
        '*.sqlite3',
        '*.log',
        '*.pot',
        '*.py[cod]',
        '*$py.class',
        '*.spec',
        '.DS_Store',
        'Thumbs.db',
        '.env',
        '*.bak',
        '*.swp',
        '*.swo',
        '*~'
    ]

    root_dir = Path('.')
    removed_dirs = 0
    removed_files = 0

    # Eliminar directorios
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

    # Eliminar archivos
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

    # Limpiar git
    print("\n🧹 Limpiando Git...")
    try:
        os.system('git clean -fdX')  # Elimina archivos no rastreados e ignorados
        print("✓ Git limpiado exitosamente")
    except Exception as e:
        print(f"✗ Error limpiando Git: {e}")

    print("\n✨ Limpieza completada!")
    print(f"  - Directorios eliminados: {removed_dirs}")
    print(f"  - Archivos eliminados: {removed_files}")

if __name__ == "__main__":
    try:
        clean_project()
        print("\n✅ Proyecto listo para commit!")
        print("\nPara completar la limpieza, ejecuta estos comandos:")
        print("1. git rm -r --cached .")
        print("2. git add .")
        print("3. git commit -m 'Clean repo and remove cached files'")
    except Exception as e:
        print(f"\n❌ Error durante la limpieza: {e}")
        sys.exit(1)