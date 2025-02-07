import sys
import pkg_resources
import platform
import os

def check_python_version():
    """Verificar versión de Python"""
    required_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        print(f"Error: Se requiere Python {required_version[0]}.{required_version[1]} o superior")
        print(f"Versión actual: {current_version[0]}.{current_version[1]}")
        return False
    return True

def check_dependencies():
    """Verificar dependencias instaladas"""
    with open('requirements.txt') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    missing = []
    for requirement in requirements:
        try:
            pkg_resources.require(requirement)
        except pkg_resources.DistributionNotFound:
            missing.append(requirement)
    
    if missing:
        print("Faltan las siguientes dependencias:")
        for pkg in missing:
            print(f"  - {pkg}")
        return False
    return True

def check_directories():
    """Verificar estructura de directorios"""
    required_dirs = [
        'src',
        'src/templates',
        'src/static',
        'src/models',
        'src/routes',
        'src/utils'
    ]
    
    missing = []
    for directory in required_dirs:
        if not os.path.exists(directory):
            missing.append(directory)
    
    if missing:
        print("Faltan los siguientes directorios:")
        for dir in missing:
            print(f"  - {dir}")
        return False
    return True

def main():
    print("Verificando configuración del sistema...")
    
    checks = [
        ("Versión de Python", check_python_version),
        ("Dependencias", check_dependencies),
        ("Estructura de directorios", check_directories)
    ]
    
    all_passed = True
    for name, check in checks:
        print(f"\nVerificando {name}...")
        if check():
            print(f"✓ {name} OK")
        else:
            print(f"✗ {name} ERROR")
            all_passed = False
    
    if all_passed:
        print("\n✓ Todo está correctamente configurado")
        return 0
    else:
        print("\n✗ Se encontraron errores en la configuración")
        return 1

if __name__ == "__main__":
    sys.exit(main())