# FinancialAR OSINT
# Copyright (C) 2025 Lucas Desimone
# Licensed under the GNU Affero General Public License v3.0
# See the LICENSE file for details.

# Templates de correo phishing educativo por banco
# SOCIAL ENGINEERING VILLAGE 2025

import base64
import os

# ============================================================================
# CAMPOS DE LOGIN POR BANCO (para landing pages dinámicas)
# ============================================================================

CAMPOS_LOGIN_BANCOS = {
    'GALICIA': {
        'titulo': 'Iniciar sesión',
        'campos': [
            {'nombre': 'dni', 'label': 'Tu DNI', 'placeholder': '', 'tipo': 'text'},
            {'nombre': 'usuario', 'label': 'Tu usuario Galicia', 'placeholder': '', 'tipo': 'text'},
            {'nombre': 'clave', 'label': 'Tu clave Galicia', 'placeholder': '', 'tipo': 'password'}
        ],
        'extras': ['Recordar DNI y Usuario', 'Teclado Virtual'],
        'boton': 'INICIAR SESIÓN',
        'links': ['OLVIDÉ O BLOQUEÉ MIS CLAVES', 'CREÁ TUS CLAVES']
    },
    'BBVA': {
        'titulo': '¡Hola! Te damos la bienvenida a Banca Online',
        'campos': [
            {'nombre': 'tipo_doc', 'label': 'Tipo de documento', 'placeholder': 'DNI', 'tipo': 'select', 'opciones': ['DNI', 'CUIT', 'CUIL']},
            {'nombre': 'documento', 'label': 'Número de documento', 'placeholder': 'Número de documento', 'tipo': 'text'},
            {'nombre': 'usuario', 'label': 'Usuario', 'placeholder': 'Usuario', 'tipo': 'text'},
            {'nombre': 'clave', 'label': 'Clave Digital', 'placeholder': 'Clave Digital', 'tipo': 'password'}
        ],
        'extras': ['Recordar mi documento y usuario', 'Teclado virtual'],
        'boton': 'Ingresar',
        'links': ['¿Olvidaste o bloqueaste tu Usuario y/o Clave Digital?', 'Si es la primera vez que ingresas a Banca Online, regístrate']
    },
    'SUPERVIELLE': {
        'titulo': 'Iniciar sesión en Online Banking Personas',
        'campos': [
            {'nombre': 'documento', 'label': 'Tu número de documento', 'placeholder': '', 'tipo': 'text'},
            {'nombre': 'usuario', 'label': 'Tu nombre de usuario', 'placeholder': '', 'tipo': 'text'},
            {'nombre': 'clave', 'label': 'Tu clave', 'placeholder': '', 'tipo': 'password'}
        ],
        'extras': ['Recordar mi número de documento', 'Teclado virtual'],
        'boton': 'Ingresar',
        'links': ['Cambiar usuario y/o clave', 'Si sos nuevo regístrate']
    },
    'CENCOSUD': {
        'titulo': 'Ingresá tu DNI, e-mail o teléfono para iniciar sesión',
        'campos': [
            {'nombre': 'documento', 'label': 'Número de Documento', 'placeholder': '', 'tipo': 'text', 'icono': '📄'},
            {'nombre': 'clave', 'label': 'Contraseña', 'placeholder': '', 'tipo': 'password', 'icono': '🔑'}
        ],
        'extras': [],
        'boton': 'Entrar',
        'links': ['¿Olvidaste tu contraseña?']
    },
    'COMAFI': {
        'titulo': '¡Hola!',
        'campos': [
            {'nombre': 'usuario', 'label': 'Ingresá tu Usuario', 'placeholder': '', 'tipo': 'text'},
            {'nombre': 'clave', 'label': 'Ingresá tu Contraseña', 'placeholder': '', 'tipo': 'password'}
        ],
        'extras': ['Recordar Usuario'],
        'boton': 'Ingresar',
        'links': ['Olvidé mis credenciales', 'Mi usuario fue bloqueado', '¡Registrate ahora!']
    },
    'CREDICOOP': {
        'titulo': 'Te damos la bienvenida a la BANCA CREDICOOP',
        'campos': [
            {'nombre': 'documento', 'label': 'Documento', 'placeholder': 'Ingresar documento', 'tipo': 'text'},
            {'nombre': 'clave', 'label': 'Clave', 'placeholder': 'Ingresar clave', 'tipo': 'password'},
            {'nombre': 'usuario', 'label': 'Usuario', 'placeholder': 'Ingresar usuario', 'tipo': 'text'}
        ],
        'extras': ['Recordar mi usuario', 'Teclado Virtual'],
        'boton': 'Ingresar',
        'links': ['Crear clave y usuario', 'Sugerencias de Seguridad']
    },
    'HIPOTECARIO': {
        'titulo': '¡Hola, somos el Banco del Hogar!',
        'campos': [
            {'nombre': 'documento', 'label': 'Documento *', 'placeholder': '', 'tipo': 'text'},
            {'nombre': 'usuario', 'label': 'Usuario', 'placeholder': '', 'tipo': 'text'},
            {'nombre': 'clave', 'label': 'Clave Búho Fácil', 'placeholder': '', 'tipo': 'password', 'info': '¿Qué es la Clave Búho Fácil?'}
        ],
        'extras': ['Recordar mi documento', 'Teclado virtual'],
        'boton': 'INGRESAR',
        'links': ['Recupero de usuario o clave', 'Soy cliente, generar usuario y clave', 'Mi cuenta está en riesgo']
    },
    'ICBC': {
        'titulo': 'ACCESS BANKING',
        'campos': [
            {'nombre': 'usuario', 'label': 'Usuario', 'placeholder': '', 'tipo': 'text'},
            {'nombre': 'clave', 'label': 'Clave', 'placeholder': '', 'tipo': 'password'}
        ],
        'extras': ['Teclado virtual'],
        'boton': 'INGRESAR',
        'links': ['No puedo ingresar', 'Tengo una clave provisoria']
    },
    'MACRO': {
        'titulo': 'Ingresá a Banca Internet',
        'subtitulo': 'Ingresá tu usuario',
        'campos': [
            {'nombre': 'usuario', 'label': 'Usuario Banca Móvil/Internet', 'placeholder': '', 'tipo': 'text'}
        ],
        'extras': ['Teclado Virtual'],
        'boton': 'Ingresá',
        'links': ['¿No podés ingresar o sos nuevo?']
    },
    'MERCADO PAGO': {
        'titulo': 'Ingresá tu DNI, e-mail o teléfono para iniciar sesión',
        'campos': [
            {'nombre': 'identificacion', 'label': 'DNI, e-mail o teléfono', 'placeholder': '', 'tipo': 'text'}
        ],
        'extras': [],
        'boton': 'Continuar',
        'links': ['Tengo un problema de seguridad', 'Necesito ayuda']
    },
    'MERCADOPAGO': {  # Alias sin espacio
        'titulo': 'Ingresá tu DNI, e-mail o teléfono para iniciar sesión',
        'campos': [
            {'nombre': 'identificacion', 'label': 'DNI, e-mail o teléfono', 'placeholder': '', 'tipo': 'text'}
        ],
        'extras': [],
        'boton': 'Continuar',
        'links': ['Tengo un problema de seguridad', 'Necesito ayuda']
    },
    'SANTANDER': {
        'titulo': '¡Hola! Te damos la bienvenida',
        'subtitulo': 'Completá tus datos y empezá a operar',
        'campos': [
            {'nombre': 'documento', 'label': 'Número de documento', 'placeholder': '', 'tipo': 'text'},
            {'nombre': 'clave', 'label': 'Contraseña', 'placeholder': '', 'tipo': 'password'},
            {'nombre': 'usuario', 'label': 'Usuario', 'placeholder': '', 'tipo': 'text'}
        ],
        'extras': ['Recordar el número de documento'],
        'boton': 'Ingresar',
        'links': ['¿Necesitás ayuda para ingresar?']
    },
    'PROVINCIA': {
        'titulo': 'Banca Internet Provincia',
        'campos': [
            {'nombre': 'documento', 'label': 'Documento', 'placeholder': 'Ingrese su documento', 'tipo': 'text'},
            {'nombre': 'usuario', 'label': 'Usuario', 'placeholder': 'Ingrese su usuario', 'tipo': 'text'},
            {'nombre': 'clave', 'label': 'Clave', 'placeholder': 'Ingrese su clave', 'tipo': 'password'}
        ],
        'extras': ['Recordar usuario'],
        'boton': 'Ingresar',
        'links': ['¿Olvidó su clave?', 'Registrarse']
    },
    'NACION': {
        'titulo': 'Banca Internet - Banco Nación',
        'campos': [
            {'nombre': 'documento', 'label': 'CUIL / CUIT', 'placeholder': '', 'tipo': 'text'},
            {'nombre': 'usuario', 'label': 'Usuario', 'placeholder': '', 'tipo': 'text'},
            {'nombre': 'clave', 'label': 'Clave de Internet', 'placeholder': '', 'tipo': 'password'}
        ],
        'extras': ['Recordar CUIL/CUIT y Usuario'],
        'boton': 'Ingresar',
        'links': ['¿Olvidó su clave?', 'Usuarios sin registrar']
    },
    'TARJETA NARANJA': {
        'titulo': 'Ingresá a Naranja Online',
        'campos': [
            {'nombre': 'email', 'label': 'Email', 'placeholder': 'Ingresá tu email', 'tipo': 'email'},
            {'nombre': 'clave', 'label': 'Clave', 'placeholder': 'Ingresá tu clave', 'tipo': 'password'}
        ],
        'extras': ['Recordar mi email'],
        'boton': 'Ingresar',
        'links': ['¿Olvidaste tu clave?', 'Registrate']
    },
    'NARANJA': {
        'titulo': 'Ingresá a Naranja Online',
        'campos': [
            {'nombre': 'email', 'label': 'Email', 'placeholder': 'Ingresá tu email', 'tipo': 'email'},
            {'nombre': 'clave', 'label': 'Clave', 'placeholder': 'Ingresá tu clave', 'tipo': 'password'}
        ],
        'extras': ['Recordar mi email'],
        'boton': 'Ingresar',
        'links': ['¿Olvidaste tu clave?', 'Registrate']
    },
    'GENERICO': {  # Fallback para bancos no configurados
        'titulo': 'Iniciar sesión',
        'campos': [
            {'nombre': 'usuario', 'label': 'Usuario', 'placeholder': '', 'tipo': 'text'},
            {'nombre': 'clave', 'label': 'Contraseña', 'placeholder': '', 'tipo': 'password'}
        ],
        'extras': [],
        'boton': 'Ingresar',
        'links': []
    }
}

# Mapeo de nombres de bancos a archivos de logo
# Importar configuración centralizada de bancos
from config.bancos_config import LOGOS_BANCOS, COLORES_BANCOS

def normalizar_nombre_banco(nombre_banco):
    """
    Normaliza nombres de bancos del BCRA a nombres cortos reconocibles
    Usa la configuración centralizada de bancos
    """
    from config.bancos_config import normalizar_nombre_banco as normalizar_central
    return normalizar_central(nombre_banco)

def obtener_logo_banco_base64(nombre_banco):
    """Convierte el logo PNG del banco a base64"""
    # Normalizar el nombre del banco primero
    nombre_normalizado = normalizar_nombre_banco(nombre_banco)
    nombre_upper = nombre_normalizado.upper()
    
    # Detectar el banco por palabras clave
    banco_key = None
    
    for key in LOGOS_BANCOS.keys():
        if key in nombre_upper or nombre_upper in key:
            banco_key = key
            break
    
    if not banco_key:
        return None
    
    # Ruta al logo
    logo_path = os.path.join('static', 'images', LOGOS_BANCOS[banco_key])
    
    try:
        with open(logo_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except:
        return None

def obtener_color_banco(nombre_banco):
    """Obtiene el color corporativo del banco"""
    # Normalizar el nombre del banco primero
    nombre_normalizado = normalizar_nombre_banco(nombre_banco)
    nombre_upper = nombre_normalizado.upper()
    
    for key, color in COLORES_BANCOS.items():
        if key in nombre_upper or nombre_upper in key:
            return color
    
    return '#000000'  # Color por defecto (negro) para bancos no listados

def generar_template_banco(nombre_banco, nombre_usuario, monto_deuda, fecha_vencimiento):
    """Template universal para todos los bancos"""
    from config.bancos_config import get_email_fake_banco, get_telefono_fake_banco
    
    logo_base64 = obtener_logo_banco_base64(nombre_banco)
    color_banco = obtener_color_banco(nombre_banco)
    email_fake = get_email_fake_banco(nombre_banco)
    telefono_fake = get_telefono_fake_banco(nombre_banco)
    
    # Generar URL de la landing page de phishing
    banco_slug = nombre_banco.lower().replace(' ', '_').replace('.', '').replace('s.a', '').replace('_de_', '_')
    landing_url = f"http://localhost:5050/phishing/{banco_slug}"
    
    # Si no hay logo, usar el nombre del banco con color de fondo
    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="{nombre_banco}">'
    else:
        # Fallback con gradiente de color
        logo_html = f'''<div style="background: linear-gradient(135deg, {color_banco} 0%, {color_banco}dd 100%); padding: 30px 20px;">
            <h1 style="margin: 0; color: white; font-size: 28px;">{nombre_banco}</h1>
            <div style="font-size: 12px; color: rgba(255,255,255,0.9); margin-top: 10px; text-transform: uppercase; letter-spacing: 1px;">Departamento de Cobranzas</div>
        </div>'''
    
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{nombre_banco} - Deuda Pendiente</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            background-color: #ffffff;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        .header {{
            padding: 0;
            text-align: center;
            overflow: hidden;
        }}
        .header img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .content {{
            padding: 40px 30px;
        }}
        .saludo {{
            font-size: 18px;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 20px;
        }}
        .alert-box {{
            background-color: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .alert-title {{
            font-weight: 700;
            color: #92400e;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .alert-text {{
            color: #78350f;
            font-size: 14px;
            line-height: 1.5;
        }}
        .deuda-info {{
            background-color: #f9fafb;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            padding: 20px;
            margin: 25px 0;
        }}
        .deuda-label {{
            font-size: 13px;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
            text-align: center;
        }}
        .deuda-monto {{
            font-size: 36px;
            font-weight: 700;
            color: {color_banco};
            margin: 10px 0;
            text-align: center;
        }}
        .deuda-detalles {{
            margin-top: 15px;
            font-size: 14px;
            color: #374151;
        }}
        .deuda-detalles li {{
            margin: 8px 0;
        }}
        .cta-button {{
            display: inline-block;
            background: linear-gradient(135deg, {color_banco} 0%, {color_banco}dd 100%);
            color: white;
            padding: 16px 40px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 16px;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }}
        .warning-text {{
            background-color: #fee2e2;
            border-left: 4px solid #dc2626;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
            font-size: 14px;
            color: #991b1b;
        }}
        .footer {{
            background-color: #f9fafb;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #e5e7eb;
        }}
        .footer-text {{
            font-size: 12px;
            color: #6b7280;
            line-height: 1.6;
            margin: 5px 0;
        }}
        .contact-info {{
            margin: 20px 0;
            padding: 15px;
            background-color: #ffffff;
            border-radius: 6px;
        }}
        .contact-item {{
            font-size: 13px;
            color: #374151;
            margin: 8px 0;
        }}
        .contact-label {{
            font-weight: 600;
            color: {color_banco};
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header con Logo -->
        <div class="header">
            {logo_html}
        </div>

        <!-- Contenido Principal -->
        <div class="content">
            <div class="saludo">
                Estimado/a {nombre_usuario},
            </div>

            <!-- Alerta de Deuda -->
            <div class="alert-box">
                <div class="alert-title">
                    ⚠️ DEUDA PENDIENTE IDENTIFICADA
                </div>
                <div class="alert-text">
                    Hemos detectado una deuda pendiente en su cuenta que requiere atención inmediata.
                </div>
            </div>

            <p style="color: #374151; line-height: 1.6;">
                Hemos identificado una deuda pendiente en su cuenta con <strong>{nombre_banco}</strong> 
                por el siguiente monto:
            </p>

            <!-- Información de la Deuda -->
            <div class="deuda-info">
                <div class="deuda-label">Monto Total Adeudado</div>
                <div class="deuda-monto">${monto_deuda}</div>
                
                <div class="deuda-detalles">
                    <strong>Detalles de la deuda:</strong>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        <li><strong>Fecha de vencimiento:</strong> {fecha_vencimiento}</li>
                        <li><strong>Estado:</strong> Pendiente de pago</li>
                        <li><strong>Intereses acumulados:</strong> Aplicables</li>
                    </ul>
                </div>
            </div>

            <!-- Advertencia de Vencimiento -->
            <div class="warning-text">
                <strong>⏰ ATENCIÓN:</strong> La fecha de vencimiento ha expirado. 
                Se están acumulando intereses adicionales. Le recomendamos regularizar su situación 
                lo antes posible para evitar mayores cargos.
            </div>

            <p style="color: #374151; line-height: 1.6;">
                Para regularizar su situación y evitar acciones legales adicionales, 
                por favor proceda con el pago a la brevedad posible.
            </p>

            <!-- Botón de Acción -->
            <div style="text-align: center; margin: 30px 0;">
                <a href="{landing_url}" class="cta-button" target="_blank">
                    REGULARIZAR DEUDA AHORA
                </a>
            </div>

            <!-- Información de Contacto -->
            <div class="contact-info">
                <div class="contact-item">
                    <span class="contact-label">📞 Teléfono:</span> {telefono_fake}
                </div>
                <div class="contact-item">
                    <span class="contact-label">✉️ Email:</span> {email_fake}
                </div>
                <div class="contact-item">
                    <span class="contact-label">🕐 Horario de atención:</span> Lunes a Viernes de 9:00 a 18:00 hs
                </div>
            </div>

            <p style="color: #6b7280; font-size: 13px; line-height: 1.6; margin-top: 30px;">
                Agradecemos su pronta atención a este asunto. Si ya ha realizado el pago, 
                por favor ignore este mensaje.
            </p>
        </div>

        <!-- Footer -->
        <div class="footer">
            <div class="footer-text">
                <strong>{nombre_banco}</strong>
            </div>
            <div class="footer-text">
                Departamento de Cobranzas y Gestión de Cuentas
            </div>
            <div class="footer-text" style="margin-top: 15px;">
                Este es un correo automático, por favor no responda a esta dirección.
            </div>
            <div class="footer-text" style="margin-top: 10px; font-size: 11px;">
                © 2025 {nombre_banco}. Todos los derechos reservados.
            </div>
            <div class="footer-text" style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #e5e7eb;">
                <strong>CONFIDENCIALIDAD:</strong> Este mensaje y sus anexos se dirigen exclusivamente 
                a su destinatario. Puede contener información privilegiada o confidencial y no puede 
                ser usado o divulgado por personas distintas de su destinatario.
            </div>
        </div>
    </div>
</body>
</html>
"""

def obtener_template_por_banco(banco, nombre_usuario, monto_deuda, fecha_vencimiento):
    """
    Retorna el template de correo phishing educativo según el banco
    Ahora usa un template universal con logos reales
    """
    return generar_template_banco(banco, nombre_usuario, monto_deuda, fecha_vencimiento)
