# FinancialAR OSINT
# Copyright (C) 2025 Lucas Desimone
# Licensed under the GNU Affero General Public License v3.0
# See the LICENSE file for details.

"""
Servicio para gestión de phishing educativo

Encapsula toda la lógica relacionada con:
- Generación de landing pages de phishing
- Generación de emails de phishing
- Configuración de campos de login por banco
- Normalización y detección de bancos
"""

from templates.email_templates import (
    LOGOS_BANCOS, 
    COLORES_BANCOS, 
    CAMPOS_LOGIN_BANCOS,
    normalizar_nombre_banco,
    generar_template_banco
)


class PhishingService:
    """Servicio para lógica de phishing educativo"""
    
    # Mapeo de nombres legibles por banco
    NOMBRES_BANCOS = {
        'GALICIA': 'Banco Galicia',
        'BBVA': 'BBVA Argentina',
        'PROVINCIA': 'Banco Provincia',
        'SANTANDER': 'Banco Santander',
        'ICBC': 'ICBC Argentina',
        'SUPERVIELLE': 'Banco Supervielle',
        'CENCOSUD': 'Cencosud',
        'MERCADO PAGO': 'Mercado Pago',
        'MERCADOPAGO': 'Mercado Pago',
        'NACION': 'Banco Nación',
        'HIPOTECARIO': 'Banco Hipotecario',
        'CREDICOOP': 'Banco Credicoop',
        'COMAFI': 'Banco Comafi',
        'MACRO': 'Banco Macro',
        'TARJETA NARANJA': 'Tarjeta Naranja',
        'NARANJA': 'Tarjeta Naranja',
    }
    
    # Campos de login genéricos (fallback)
    CAMPOS_LOGIN_GENERICOS = {
        'titulo': 'Iniciar sesión',
        'campos': [
            {'nombre': 'usuario', 'label': 'Usuario', 'placeholder': 'Ingrese su usuario', 'tipo': 'text'},
            {'nombre': 'clave', 'label': 'Contraseña', 'placeholder': 'Ingrese su contraseña', 'tipo': 'password'}
        ],
        'extras': [],
        'boton': 'Ingresar',
        'links': []
    }
    
    @staticmethod
    def limpiar_nombre_banco(nombre_banco):
        """
        Limpia el nombre del banco de caracteres especiales
        
        Args:
            nombre_banco: Nombre del banco con caracteres especiales
            
        Returns:
            str: Nombre limpio
        """
        return nombre_banco.replace('_', ' ').replace('(', '').replace(')', '').strip()
    
    @staticmethod
    def detectar_banco_key(nombre_banco):
        """
        Detecta la clave del banco basándose en el nombre
        
        Args:
            nombre_banco: Nombre del banco a detectar
            
        Returns:
            str|None: Clave del banco o None si no se encuentra
        """
        # Normalizar el nombre del banco
        banco_normalizado = normalizar_nombre_banco(nombre_banco)
        banco_upper = banco_normalizado.upper()
        
        # Buscar coincidencia en logos
        for key in LOGOS_BANCOS.keys():
            if key in banco_upper or banco_upper in key:
                return key
        
        return None
    
    @staticmethod
    def obtener_nombre_legible(banco_key, nombre_fallback):
        """
        Obtiene el nombre legible del banco
        
        Args:
            banco_key: Clave del banco
            nombre_fallback: Nombre a usar si no se encuentra
            
        Returns:
            str: Nombre legible del banco
        """
        return PhishingService.NOMBRES_BANCOS.get(
            banco_key, 
            nombre_fallback.replace('_', ' ').title()
        )
    
    @staticmethod
    def obtener_campos_login(banco_key, banco_nombre):
        """
        Obtiene la configuración de campos de login para un banco
        
        Args:
            banco_key: Clave del banco
            banco_nombre: Nombre del banco para personalización
            
        Returns:
            dict: Configuración de campos de login
        """
        # Intentar obtener campos específicos del banco
        campos = CAMPOS_LOGIN_BANCOS.get(banco_key)
        
        # Si no hay campos definidos, usar genérico personalizado
        if not campos:
            campos = PhishingService.CAMPOS_LOGIN_GENERICOS.copy()
            campos['titulo'] = f'Iniciar sesión en {banco_nombre}'
        
        return campos
    
    @classmethod
    def obtener_datos_landing_phishing(cls, nombre_banco):
        """
        Obtiene todos los datos necesarios para renderizar landing de phishing
        
        Args:
            nombre_banco: Nombre del banco recibido en URL
            
        Returns:
            dict: Datos completos para renderizar template
        """
        # Limpiar nombre
        banco_limpio = cls.limpiar_nombre_banco(nombre_banco)
        
        # Detectar banco
        banco_key = cls.detectar_banco_key(banco_limpio)
        
        # Caso genérico (banco no encontrado)
        if not banco_key:
            return {
                'banco_nombre': banco_limpio.title(),
                'logo_archivo': None,
                'color_banco': '#000000',
                'campos': cls.CAMPOS_LOGIN_GENERICOS['campos'],
                'titulo': cls.CAMPOS_LOGIN_GENERICOS['titulo'],
                'subtitulo': '',
                'extras': [],
                'texto_boton': cls.CAMPOS_LOGIN_GENERICOS['boton'],
                'links_adicionales': []
            }
        
        # Banco encontrado: obtener configuración
        banco_nombre = cls.obtener_nombre_legible(banco_key, banco_limpio)
        logo_archivo = LOGOS_BANCOS.get(banco_key)
        color_banco = COLORES_BANCOS.get(banco_key, '#000000')
        campos_login = cls.obtener_campos_login(banco_key, banco_nombre)
        
        return {
            'banco_nombre': banco_nombre,
            'logo_archivo': logo_archivo,
            'color_banco': color_banco,
            'campos': campos_login['campos'],
            'titulo': campos_login['titulo'],
            'subtitulo': campos_login.get('subtitulo', ''),
            'extras': campos_login.get('extras', []),
            'texto_boton': campos_login.get('boton', 'Ingresar'),
            'links_adicionales': campos_login.get('links', [])
        }
    
    @staticmethod
    def generar_email_phishing(banco, nombre_usuario, monto_deuda, fecha_vencimiento):
        """
        Genera el HTML de un email de phishing educativo
        
        Args:
            banco: Nombre del banco
            nombre_usuario: Nombre del destinatario
            monto_deuda: Monto de la deuda
            fecha_vencimiento: Fecha de vencimiento
            
        Returns:
            str: HTML del email de phishing
        """
        return generar_template_banco(
            nombre_banco=banco,
            nombre_usuario=nombre_usuario,
            monto_deuda=monto_deuda,
            fecha_vencimiento=fecha_vencimiento
        )

