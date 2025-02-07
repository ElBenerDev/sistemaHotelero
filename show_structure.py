import os
from pathlib import Path

def print_tree(directory, prefix="", exclude_dirs=None, exclude_files=None):
    """
    Imprime la estructura de directorios en formato árbol
    """
    if exclude_dirs is None:
        exclude_dirs = {'.git', '__pycache__', 'venv', 'env', 'dist', 'build'}
    if exclude_files is None:
        exclude_files = {'.gitignore', '.pyc', '.pyo', '.pyd', '.spec'}
    
    # Obtener elementos del directorio
    paths = sorted(Path(directory).glob('*'))
    
    # Filtrar elementos excluidos
    paths = [p for p in paths 
            if not any(ex in str(p) for ex in exclude_dirs)
            and not any(p.name.endswith(ex) for ex in exclude_files)]
    
    # Procesar cada elemento
    for i, path in enumerate(paths):
        is_last = i == len(paths) - 1
        node = "└── " if is_last else "├── "
        
        print(f"{prefix}{node}{path.name}")
        
        if path.is_dir():
            extension = "    " if is_last else "│   "
            print_tree(path, prefix + extension, exclude_dirs, exclude_files)

if __name__ == "__main__":
    print("\n📁 Estructura del Proyecto:")
    print(".")
    print_tree(".")