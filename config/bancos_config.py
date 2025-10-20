# FinancialAR OSINT
# Copyright (C) 2025 Lucas Desimone
# Licensed under the GNU Affero General Public License v3.0
# See the LICENSE file for details.

"""
Configuración centralizada de bancos argentinos
Single Source of Truth para toda la aplicación
Social Engineering Village 2025
"""

# ============================================================
# CONFIGURACIÓN COMPLETA DE BANCOS
# ============================================================

BANCOS_CONFIG = {
    'GALICIA': {
        'nombre_completo': 'Banco Galicia',
        'nombre_oficial': 'BANCO DE GALICIA Y BUENOS AIRES',        
        'logo': 'banco_galicia.png',
        'color': '#ff6601',
        'email_fake': 'cobranzas.galicia@secure-verify.com',
        'telefono_fake': '0800-555-4242',
    },
    'BBVA': {
        'nombre_completo': 'BBVA Argentina',
        'nombre_oficial': 'BBVA BANCO FRANCES',        
        'logo': 'banco_bbva.png',
        'color': '#19549b',
        'email_fake': 'recuperos.bbva@banking-secure.net',
        'telefono_fake': '0800-777-2828',
    },
    'PROVINCIA': {
        'nombre_completo': 'Banco Provincia',
        'nombre_oficial': 'BANCO DE LA PROVINCIA DE BUENOS AIRES',        
        'logo': 'banco_provincia.png',
        'color': '#279d2e',
        'email_fake': 'recuperos.bapro@secure-banking.com',
        'telefono_fake': '0800-333-2776',
    },
    'SANTANDER': {
        'nombre_completo': 'Banco Santander',
        'nombre_oficial': 'BANCO SANTANDER RIO',        
        'logo': 'banco_santander.png',
        'color': '#fe0000',
        'email_fake': 'recuperos.santander@secure-banking.net',
        'telefono_fake': '0800-999-4444',
    },
    'ICBC': {
        'nombre_completo': 'ICBC Argentina',
        'nombre_oficial': 'INDUSTRIAL AND COMMERCIAL BANK OF CHINA',        
        'logo': 'banco_icbc.png',
        'color': '#ca0202',
        'email_fake': 'cobranzas.icbc@banking-verify.net',
        'telefono_fake': '0800-444-4422',
    },
    'SUPERVIELLE': {
        'nombre_completo': 'Banco Supervielle',
        'nombre_oficial': 'BANCO SUPERVIELLE',        
        'logo': 'banco_supervielle.png',
        'color': '#fe0000',
        'email_fake': 'recuperos.supervielle@secure-bank.com',
        'telefono_fake': '0800-555-7777',
    },
    'CENCOSUD': {
        'nombre_completo': 'Cencosud',
        'nombre_oficial': 'CENCOSUD',        
        'logo': 'banco_cencosud.png',
        'color': '#0901c4',
        'email_fake': 'cobranzas.cencosud@verificacion-online.com',
        'telefono_fake': '0800-999-2362',
    },
    'MERCADOPAGO': {
        'nombre_completo': 'Mercado Pago',
        'nombre_oficial': 'MERCADO PAGO',        
        'logo': 'banco_mercado_pago.png',
        'color': '#01bbfe',
        'email_fake': 'cobranzas.mercadopago@verify-account.net',
        'telefono_fake': '0800-777-6727',
    },
    'NACION': {
        'nombre_completo': 'Banco Nación',
        'nombre_oficial': 'BANCO DE LA NACION ARGENTINA',        
        'logo': 'banco_nacion.png',
        'color': '#0f7391',
        'email_fake': 'cobranzas.bna@verificacion-segura.com',
        'telefono_fake': '0800-666-8100',
    },
    'HIPOTECARIO': {
        'nombre_completo': 'Banco Hipotecario',
        'nombre_oficial': 'BANCO HIPOTECARIO',        
        'logo': 'banco_hipotecario.png',
        'color': '#f47321',
        'email_fake': 'recuperos.hipotecario@secure-verify.com',
        'telefono_fake': '0800-888-4476',
    },
    'CREDICOOP': {
        'nombre_completo': 'Banco Credicoop',
        'nombre_oficial': 'BANCO CREDICOOP',        
        'logo': 'banco_credicoop.png',
        'color': '#737173',
        'email_fake': 'cobranzas.credicoop@banking-secure.net',
        'telefono_fake': '0800-666-7777',
    },
    'COMAFI': {
        'nombre_completo': 'Banco Comafi',
        'nombre_oficial': 'BANCO COMAFI',        
        'logo': 'banco_comafi.png',
        'color': '#97ad6a',
        'email_fake': 'recuperos.comafi@verify-secure.com',
        'telefono_fake': '0800-555-9999',
    },
    'MACRO': {
        'nombre_completo': 'Banco Macro',
        'nombre_oficial': 'BANCO MACRO',        
        'logo': 'banco_macro.png',
        'color': '#232b54',
        'email_fake': 'cobranzas.macro@secure-banking.com',
        'telefono_fake': '0800-999-8888',
    },
    'ITAU': {
        'nombre_completo': 'Banco Itaú',
        'nombre_oficial': 'BANCO ITAU',        
        'logo': None,  # Sin logo disponible
        'color': '#ec7000',
        'email_fake': 'recuperos.itau@banking-verify.net',
        'telefono_fake': '0800-777-3456',
    },
    'PATAGONIA': {
        'nombre_completo': 'Banco Patagonia',
        'nombre_oficial': 'BANCO PATAGONIA',        
        'logo': None,  # Sin logo disponible
        'color': '#004280',
        'email_fake': 'recuperos.patagonia@banking-secure.com',
        'telefono_fake': '0800-666-5555',
    },
    'NARANJA': {
        'nombre_completo': 'Tarjeta Naranja',
        'nombre_oficial': 'TARJETA NARANJA',        'logo': 'tarjeta_naranja.png',
        'color': '#4d0579',
        # Datos fake para phishing educativo
        'email_fake': 'cobranzas.naranja@verify-account.com',
        'telefono_fake': '0800-555-6272',
    },
}

# ============================================================
# VISTAS DERIVADAS (para compatibilidad con código existente)
# ============================================================


def get_logos_bancos():
    """
    Devuelve dict con logos (formato email_templates.py anterior)
    """
    return {
        key: config['logo']
        for key, config in BANCOS_CONFIG.items()
        if config['logo'] is not None
    }

def get_colores_bancos():
    """
    Devuelve dict con colores (formato email_templates.py anterior)
    """
    return {
        key: config['color']
        for key, config in BANCOS_CONFIG.items()
    }

def get_nombres_bancos():
    """
    Devuelve dict con nombres legibles (formato bancos_nombres.py anterior)
    """
    return {
        key: config['nombre_completo']
        for key, config in BANCOS_CONFIG.items()
    }

def get_banco_info(nombre_banco):
    """
    Busca información de un banco por nombre (flexible)
    
    Args:
        nombre_banco: Nombre del banco (puede ser clave, nombre completo o nombre oficial)
        
    Returns:
        Dict con toda la información del banco o None si no se encuentra
    """
    nombre_upper = nombre_banco.upper()
    
    # Búsqueda exacta por clave
    if nombre_upper in BANCOS_CONFIG:
        return BANCOS_CONFIG[nombre_upper]
    
    # Búsqueda por nombre oficial o completo
    for key, config in BANCOS_CONFIG.items():
        if (nombre_upper in config['nombre_oficial'].upper() or 
            config['nombre_oficial'].upper() in nombre_upper or
            nombre_upper in config['nombre_completo'].upper()):
            return config
    
    return None

def normalizar_nombre_banco(nombre_banco):
    """
    Normaliza nombres de bancos del BCRA a claves cortas
    
    Args:
        nombre_banco: Nombre del banco como aparece en BCRA
        
    Returns:
        Clave normalizada del banco o el nombre original si no se encuentra
    """
    nombre_upper = nombre_banco.upper()
    
    # Mapeo directo de nombres oficiales a claves
    for key, config in BANCOS_CONFIG.items():
        if config['nombre_oficial'].upper() in nombre_upper or nombre_upper in config['nombre_oficial'].upper():
            return key
    
    # Si no se encuentra, devolver nombre original
    return nombre_banco


# ============================================================
# ALIASES (generados dinámicamente)
# ============================================================

LOGOS_BANCOS = get_logos_bancos()
COLORES_BANCOS = get_colores_bancos()
NOMBRES_BANCOS = get_nombres_bancos()

# ============================================================
# UTILIDADES
# ============================================================

def listar_bancos():
    """Lista todos los bancos configurados"""
    return list(BANCOS_CONFIG.keys())

def validar_banco(clave_banco):
    """Verifica si existe un banco con esa clave"""
    return clave_banco.upper() in BANCOS_CONFIG


def get_color_banco(nombre_banco):
    """Obtiene solo el color de un banco"""
    info = get_banco_info(nombre_banco)
    return info['color'] if info else '#000000'

def get_logo_banco(nombre_banco):
    """Obtiene solo el logo de un banco"""
    info = get_banco_info(nombre_banco)
    return info['logo'] if info else None

def get_email_fake_banco(nombre_banco):
    """Obtiene el email FAKE (para phishing educativo) de un banco"""
    info = get_banco_info(nombre_banco)
    if info and 'email_fake' in info:
        return info['email_fake']
    # Fallback si no tiene email fake configurado
    return 'cobranzas_banco@verificacion-segura.com'

def get_telefono_fake_banco(nombre_banco):
    """Obtiene el teléfono FAKE (para phishing educativo) de un banco"""
    info = get_banco_info(nombre_banco)
    if info and 'telefono_fake' in info:
        return info['telefono_fake']
    # Fallback si no tiene teléfono fake configurado
    return '0800-FAKE-CEL'

