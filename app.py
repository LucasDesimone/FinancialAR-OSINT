# FinancialAR OSINT
# Copyright (C) 2025 Lucas Desimone
# Licensed under the GNU Affero General Public License v3.0
# See the LICENSE file for details.

from flask import Flask, render_template, request, jsonify, send_file
import requests
import json
import re
from datetime import datetime
import os
import logging
from jinja2 import Template
import io
import tempfile
from templates.email_templates import obtener_template_por_banco
from utils.validators import CUITValidator, TextoSanitizer
from services import BCRAService, AFIPService

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Output a consola
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Inicializar servicios
bcra_service = BCRAService()
afip_service = AFIPService()

# Headers de seguridad
@app.after_request
def add_security_headers(response):
    """Agregar headers de seguridad a todas las respuestas"""
    # Evita que el navegador adivine el tipo MIME
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # Evita que el sitio se cargue en iframes (protección contra clickjacking)
    response.headers['X-Frame-Options'] = 'DENY'
    # Protección XSS básica del navegador
    response.headers['X-XSS-Protection'] = '1; mode=block'
    # Política de referrer (no enviar URL completa a sitios externos)
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Content Security Policy (protección contra XSS e inyección de código)
    # 'unsafe-inline' permite event handlers inline (onclick, onchange, etc.) - necesario para la app
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https://api.bcra.gob.ar; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self';"
    )
    
    # Permissions Policy (deshabilitar APIs innecesarias)
    response.headers['Permissions-Policy'] = (
        'geolocation=(), microphone=(), camera=(), payment=(), usb=()'
    )
    
    return response

# Importar configuración centralizada de bancos
from config.bancos_config import get_banco_info


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/phishing/<banco>')
def landing_phishing(banco):
    """
    Landing page de phishing educativo para cada banco
    """
    from services.phishing_service import PhishingService
    
    # Obtener datos del servicio
    datos = PhishingService.obtener_datos_landing_phishing(banco)
    
    # Renderizar template
    return render_template('landing_phishing.html', **datos)

@app.route('/consultar', methods=['POST'])
def consultar():
    """Endpoint para consultar deudas BCRA por CUIT"""
    data = request.get_json()
    cuit = data.get('cuit', '').strip()
    
    # Validar CUIT
    if not cuit:
        logger.warning("Intento de consulta sin CUIT")
        return jsonify({"error": "Debe ingresar un CUIT"}), 400
    
    try:
        CUITValidator.validar(cuit)
    except ValueError as e:
        logger.warning(f"CUIT inválido: {str(e)}")
        return jsonify({"error": str(e)}), 400
    
    # Limpiar CUIT para consulta
    cuit_limpio = CUITValidator.limpiar(cuit)
    
    # Consultar deudas usando el servicio
    resultado_api = bcra_service.consultar_deudas(cuit_limpio)
    
    if "error" in resultado_api:
        logger.error(f"Error en consulta BCRA: {resultado_api.get('error')}")
        return jsonify(resultado_api), 400
    
    # Procesar deudas por banco
    deudas = resultado_api.get("deudas", [])
    deudas_por_banco = bcra_service.procesar_deudas_por_banco(deudas)
    
    # Calcular totales
    total_deuda = sum(banco["total"] for banco in deudas_por_banco.values())
    cantidad_total = sum(banco["cantidad"] for banco in deudas_por_banco.values())
    
    return jsonify({
        "deudas_por_banco": deudas_por_banco,
        "deudas": deudas,  # Para el modal de detalles
        "total_deuda": total_deuda,
        "cantidad_total": cantidad_total,
        "bancos_afectados": len(deudas_por_banco),
        "denominacion": resultado_api.get("denominacion", ""),
        "cuit_consultado": resultado_api.get("cuit_consultado", cuit_limpio),
        "nombre": resultado_api.get("denominacion", "")  # Para compatibilidad con frontend
    })


@app.route('/visualizar_correo_phishing', methods=['POST'])
def visualizar_correo_phishing():
    """
    Genera y retorna el HTML del correo phishing para visualización
    """
    try:
        from services.phishing_service import PhishingService
        
        data = request.get_json()
        banco = data.get('banco', '')
        nombre_usuario = data.get('nombre_usuario', 'Usuario')
        monto_deuda = data.get('monto_deuda', '$0')
        fecha_vencimiento = data.get('fecha_vencimiento', 'No especificada')
        
        # Generar template usando el servicio
        template_html = PhishingService.generar_email_phishing(
            banco=banco,
            nombre_usuario=nombre_usuario,
            monto_deuda=monto_deuda,
            fecha_vencimiento=fecha_vencimiento
        )
        
        # Retornar el HTML directamente
        return template_html, 200, {'Content-Type': 'text/html; charset=utf-8'}
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/buscar_por_nombre', methods=['POST'])
def buscar_por_nombre():
    """Endpoint para buscar contribuyentes en base AFIP por nombre y apellido"""
    try:
        data = request.get_json()
        apellido = data.get('apellido', '').strip()
        nombre = data.get('nombre', '').strip()
        
        # Sanitizar inputs
        apellido = TextoSanitizer.sanitizar_busqueda(apellido, max_length=100)
        nombre = TextoSanitizer.sanitizar_busqueda(nombre, max_length=100)
        
        if not apellido:
            return jsonify({
                'success': False,
                'error': 'Debe proporcionar al menos un apellido válido'
            }), 400
        
        # Buscar usando el servicio
        resultado = afip_service.buscar_contribuyentes(apellido, nombre, limite=20)
        
        if not resultado['success']:
            return jsonify(resultado), 503 if 'no disponible' in resultado.get('error', '') else 500
        
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"Error en búsqueda por nombre: {e}")
        return jsonify({
            'success': False,
            'error': f'Error en la búsqueda: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Crear directorio de templates si no existe
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5050)
