import PyInstaller.__main__
import sys
import os

def build_exe():
    PyInstaller.__main__.run([
        'run.py',                          # Script principal
        '--name=SistemaHotelero',          # Nombre del ejecutable
        '--onefile',                       # Un solo archivo ejecutable
        '--windowed',                      # Sin consola en Windows
        '--add-data=src/templates;src/templates',  # Incluir templates
        '--add-data=src/static;src/static',       # Incluir archivos estáticos
        '--icon=src/static/img/icon.ico',  # Icono del ejecutable
        '--clean',                         # Limpiar cache
        '--noconfirm'                      # No confirmar sobrescritura
    ])

if __name__ == "__main__":
    build_exe()