#!/usr/bin/env python3
# FinancialAR OSINT
# Copyright (C) 2025 Lucas Desimone
# Licensed under the GNU Affero General Public License v3.0
# See the LICENSE file for details.

"""
FinancialAR OSINT - Herramienta de Inteligencia Financiera
Social Engineering Village 2025
"""

import os
import sys
import subprocess
import socket
import warnings
from pathlib import Path

# Suprimir warning de urllib3 sobre OpenSSL/LibreSSL
warnings.filterwarnings('ignore', message='.*urllib3 v2.*', category=Warning)

# Colores ANSI
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def get_local_ip():
    """Obtener la IP local de la máquina"""
    try:
        # Crear un socket temporal para obtener la IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "localhost"

def print_banner():
    """Mostrar banner ASCII art"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ███████╗██╗███╗   ██╗ █████╗ ███╗   ██╗ ██████╗██╗ █████╗ ██╗           ║
║   ██╔════╝██║████╗  ██║██╔══██╗████╗  ██║██╔════╝██║██╔══██╗██║           ║
║   █████╗  ██║██╔██╗ ██║███████║██╔██╗ ██║██║     ██║███████║██║           ║
║   ██╔══╝  ██║██║╚██╗██║██╔══██║██║╚██╗██║██║     ██║██╔══██║██║           ║
║   ██║     ██║██║ ╚████║██║  ██║██║ ╚████║╚██████╗██║██║  ██║███████╗      ║
║   ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚═╝╚═╝  ╚═╝╚══════╝      ║
║                                                                           ║
║        █████╗ ██████╗      ██████╗ ███████╗██╗███╗   ██╗████████╗         ║
║       ██╔══██╗██╔══██╗    ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝         ║
║       ███████║██████╔╝    ██║   ██║███████╗██║██╔██╗ ██║   ██║            ║
║       ██╔══██║██╔══██╗    ██║   ██║╚════██║██║██║╚██╗██║   ██║            ║
║       ██║  ██║██║  ██║    ╚██████╔╝███████║██║██║ ╚████║   ██║            ║
║       ╚═╝  ╚═╝╚═╝  ╚═╝     ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝            ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.YELLOW}    🔍 Herramienta de Inteligencia Financiera y Concientización OSINT{Colors.RESET}
{Colors.MAGENTA}    📍 Social Engineering Village 2025 - Ekoparty Security Conference{Colors.RESET}
{Colors.BLUE}    💻 Desarrollado por Lucas Desimone{Colors.RESET}

"""
    print(banner)

def check_python_version():
    """Verificar versión de Python"""
    if sys.version_info < (3, 8):
        print(f"{Colors.RED}❌ Error: Se requiere Python 3.8 o superior{Colors.RESET}")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"{Colors.GREEN}✅ Python {sys.version.split()[0]} detectado{Colors.RESET}")
    return True

def check_dependencies():
    """Verificar dependencias instaladas"""
    try:
        import flask
        import requests
        print(f"{Colors.GREEN}✅ Dependencias encontradas{Colors.RESET}")
        return True
    except ImportError:
        print(f"{Colors.RED}❌ Dependencias faltantes{Colors.RESET}")
        return False

def install_dependencies():
    """Instalar dependencias desde requirements.txt"""
    print(f"{Colors.YELLOW}📦 Instalando dependencias...{Colors.RESET}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print(f"{Colors.GREEN}✅ Dependencias instaladas correctamente{Colors.RESET}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}❌ Error instalando dependencias: {e}{Colors.RESET}")
        return False

def create_directories():
    """Crear directorios necesarios"""
    dirs = ['templates', 'static/css', 'static/js']
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    print(f"{Colors.GREEN}✅ Directorios creados{Colors.RESET}")

def main():
    """Función principal"""
    # Solo mostrar banner en el proceso principal (no en el reloader de Flask)
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        # Mostrar banner ASCII
        print_banner()
        
        print(f"{Colors.CYAN}{'═' * 79}{Colors.RESET}")
        print(f"{Colors.BOLD}🔍 INICIANDO SISTEMA...{Colors.RESET}\n")
        
        # Verificar Python
        if not check_python_version():
            sys.exit(1)
        
        # Crear directorios
        create_directories()
        
        # Verificar dependencias
        if not check_dependencies():
            print(f"\n{Colors.YELLOW}🔧 Instalando dependencias automáticamente...{Colors.RESET}")
            if not install_dependencies():
                print(f"\n{Colors.RED}❌ No se pudieron instalar las dependencias automáticamente{Colors.RESET}")
                print("   Ejecuta manualmente: pip install -r requirements.txt")
                sys.exit(1)
        
        # Obtener IP local
        local_ip = get_local_ip()
        
        print(f"\n{Colors.CYAN}{'═' * 79}{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}🚀 APLICACIÓN INICIADA CORRECTAMENTE{Colors.RESET}")
        print(f"\n{Colors.YELLOW}📍 URL Local:{Colors.RESET}      {Colors.BOLD}http://localhost:5050{Colors.RESET}")
        print(f"{Colors.YELLOW}📍 URL Red:{Colors.RESET}        {Colors.BOLD}http://{local_ip}:5050{Colors.RESET}")
        print(f"\n{Colors.MAGENTA}⚠️  Presiona Ctrl+C para detener el servidor{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 79}{Colors.RESET}\n")
    
    # Importar y ejecutar la aplicación
    try:
        from app import app
        # Debug mode desde variable de entorno (por defecto False)
        debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
        app.run(debug=debug_mode, host='0.0.0.0', port=5050)
    except KeyboardInterrupt:
        if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
            print(f"\n\n{Colors.YELLOW}👋 Aplicación detenida por el usuario{Colors.RESET}")
            print(f"{Colors.GREEN}✅ Shutdown exitoso{Colors.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error iniciando la aplicación: {e}{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
