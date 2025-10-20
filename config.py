# FinancialAR OSINT
# Copyright (C) 2025 Lucas Desimone
# Licensed under the GNU Affero General Public License v3.0
# See the LICENSE file for details.

"""
Configuración de la aplicación
Herramienta de Concientización de Deudas BCRA - Social Engineering Village 2025
"""

import os
import secrets
from pathlib import Path

def _get_or_create_secret_key():
    """Genera y persiste SECRET_KEY de forma segura"""
    secret_key_file = Path(__file__).parent / '.secret_key'
    
    if secret_key_file.exists():
        with open(secret_key_file, 'r') as f:
            return f.read().strip()
    
    # Generar nueva clave criptográficamente segura
    secret_key = secrets.token_urlsafe(32)
    with open(secret_key_file, 'w') as f:
        f.write(secret_key)
    
    # Solo owner puede leer (chmod 600)
    secret_key_file.chmod(0o600)
    print(f"✅ SECRET_KEY generada y guardada en {secret_key_file}")
    return secret_key

class Config:
    """Configuración base"""
    
    # Configuración de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or _get_or_create_secret_key()
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Configuración de la API del BCRA
    BCRA_API_BASE = "https://api.bcra.gob.ar/centraldedeudores/v1.0"
    BCRA_API_TIMEOUT = 30
    
    # Configuración de la aplicación
    APP_NAME = "Consulta de Deudas BCRA"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Herramienta de concientización sobre deudas bancarias"
    EKOPARTY_YEAR = "2024"
    
    # Configuración de seguridad
    MAX_CUIT_LENGTH = 13  # XX-XXXXXXXX-X
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_REQUESTS = 10  # requests per minute per IP
    
    # Configuración de UI
    ITEMS_PER_PAGE = 10
    ANIMATION_DURATION = 300  # milliseconds
    
    # Información de bancos (puede ser extendida)
    BANCOS_INFO = {
        "BANCO DE LA NACION ARGENTINA": {
            "email": "contacto@bna.com.ar",
            "telefono": "0810-810-8100",
            "website": "https://www.bna.com.ar",
            "color": "#1e40af"
        },
        "BANCO SANTANDER RIO": {
            "email": "atencion@santanderrio.com.ar",
            "telefono": "0810-444-4444",
            "website": "https://www.santanderrio.com.ar",
            "color": "#dc2626"
        },
        "BANCO GALICIA": {
            "email": "atencion@bancogalicia.com.ar",
            "telefono": "0810-810-8103",
            "website": "https://www.bancogalicia.com",
            "color": "#059669"
        },
        "BANCO MACRO": {
            "email": "atencion@bancomacro.com.ar",
            "telefono": "0810-444-4444",
            "website": "https://www.bancomacro.com.ar",
            "color": "#7c3aed"
        },
        "BANCO ITAU": {
            "email": "atencion@itau.com.ar",
            "telefono": "0810-345-3456",
            "website": "https://www.itau.com.ar",
            "color": "#ea580c"
        },
        "BANCO HSBC": {
            "email": "atencion@hsbc.com.ar",
            "telefono": "0810-444-4444",
            "website": "https://www.hsbc.com.ar",
            "color": "#0891b2"
        },
        "BANCO CREDICOOP": {
            "email": "atencion@credicoop.com.ar",
            "telefono": "0810-444-4444",
            "website": "https://www.credicoop.com.ar",
            "color": "#be185d"
        },
        "BANCO SUPERVIELLE": {
            "email": "atencion@supervielle.com.ar",
            "telefono": "0810-444-4444",
            "website": "https://www.supervielle.com.ar",
            "color": "#0d9488"
        },
        "BANCO PATAGONIA": {
            "email": "atencion@bancopatagonia.com.ar",
            "telefono": "0810-444-4444",
            "website": "https://www.bancopatagonia.com.ar",
            "color": "#dc2626"
        },
        "BANCO COMAFI": {
            "email": "atencion@comafi.com.ar",
            "telefono": "0810-444-4444",
            "website": "https://www.comafi.com.ar",
            "color": "#7c2d12"
        }
    }
    
    # Plantillas de correo personalizables
    EMAIL_TEMPLATES = {
        "default": {
            "subject": "Consulta sobre situación crediticia - {banco}",
            "greeting": "Estimados Sres. de {banco},",
            "closing": "Saludos cordiales,\n[Su nombre]"
        },
        "refinanciacion": {
            "subject": "Solicitud de refinanciación - {banco}",
            "greeting": "Estimados Sres. de {banco},",
            "closing": "Quedo a la espera de su respuesta.\nSaludos cordiales,\n[Su nombre]"
        },
        "regularizacion": {
            "subject": "Regularización de deudas - {banco}",
            "greeting": "Estimados Sres. de {banco},",
            "closing": "Agradezco su atención.\nSaludos cordiales,\n[Su nombre]"
        }
    }
    
    # Configuración de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configuración de desarrollo
    DEVELOPMENT = DEBUG
    TESTING = False

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-this-in-production'

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DEBUG = True

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
