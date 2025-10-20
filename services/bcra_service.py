# FinancialAR OSINT
# Copyright (C) 2025 Lucas Desimone
# Licensed under the GNU Affero General Public License v3.0
# See the LICENSE file for details.

"""
Servicio para consultas BCRA
Encapsula toda la lógica de negocio de consultas de deudas
"""
import requests
import time
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Configuración SSL simplificada para herramienta local
import os
import platform
import ssl
from urllib3.util.ssl_ import create_urllib3_context
from requests.adapters import HTTPAdapter

# Configuración SSL por defecto: SIN verificación (para compatibilidad universal)
# Los usuarios pueden habilitar SSL con variable de entorno: BCRA_SSL_VERIFY=true
SSL_VERIFY_DEFAULT = os.getenv('BCRA_SSL_VERIFY', 'false').lower() == 'true'

# Detectar sistema operativo para logging
SYSTEM = platform.system().lower()
IS_LINUX = 'linux' in SYSTEM

logger = logging.getLogger(__name__)

if SSL_VERIFY_DEFAULT:
    logger.info("SSL verification ENABLED (configurado por usuario)")
    # Configuración SSL completa solo si está habilitada
    try:
        import truststore
        truststore.inject_into_ssl()
        SSL_CONFIG = "truststore (certificados del sistema)"
    except ImportError:
        import certifi
        SSL_CONFIG = f"certifi ({certifi.where()})"
    
    # Contexto SSL personalizado para Linux si está habilitado
    SSL_CONTEXT = None
    if IS_LINUX:
        try:
            SSL_CONTEXT = create_urllib3_context()
            SSL_CONTEXT.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS')
            logger.info("Contexto SSL personalizado creado para Linux")
        except Exception as e:
            logger.warning(f"No se pudo crear contexto SSL personalizado: {e}")
            SSL_CONTEXT = None
else:
    logger.info("SSL verification DISABLED (configuración por defecto para compatibilidad universal)")
    SSL_CONFIG = "Sin verificación SSL (compatibilidad universal)"
    SSL_CONTEXT = None


class BCRAService:
    """Servicio para consultas a la API del BCRA"""
    
    # Configuración de la API
    API_URLS = [
        "https://api.bcra.gob.ar/centraldedeudores/v1.0/Deudas/{cuit}",
        "https://api.bcra.gob.ar/centraldedeudores/v1.0/deudas/{cuit}",
        "https://api.bcra.gob.ar/central-deudores/v1/Deudas/{cuit}",
    ]
    
    TIMEOUT = 30
    MAX_RETRIES = 3
    
    # Mapeo de situaciones del BCRA
    SITUACIONES = {
        1: {
            "descripcion": "En situación normal",
            "riesgo": "Situación normal",
            "color": "success",
            "icono": "check-circle",
            "explicacion": "Tu situación crediticia es normal. No hay problemas registrados."
        },
        2: {
            "descripcion": "Con seguimiento especial",
            "riesgo": "Riesgo bajo",
            "color": "info",
            "icono": "eye",
            "explicacion": "El banco está monitoreando tu cuenta más de cerca, pero el riesgo es bajo."
        },
        3: {
            "descripcion": "Con problemas",
            "riesgo": "Riesgo medio",
            "color": "warning",
            "icono": "exclamation-triangle",
            "explicacion": "Hay problemas en tu cuenta que requieren atención. Riesgo medio."
        },
        4: {
            "descripcion": "Con alto riesgo de insolvencia",
            "riesgo": "Riesgo alto",
            "color": "danger",
            "icono": "exclamation-circle",
            "explicacion": "Alto riesgo de insolvencia. Es importante contactar al banco urgentemente."
        },
        5: {
            "descripcion": "Irrecuperable",
            "riesgo": "Irrecuperable",
            "color": "dark",
            "icono": "times-circle",
            "explicacion": "La deuda se considera irrecuperable. Consulta opciones de refinanciación."
        }
    }
    
    def __init__(self):
        """Inicializa el servicio BCRA con configuración SSL simplificada"""
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'FinancialAR-OSINT/1.0',
            'Content-Type': 'application/json'
        })
        
        # Configuración SSL simplificada
        self._configure_ssl()
    
    def _configure_ssl(self):
        """Configura SSL de manera simple y compatible"""
        if SSL_VERIFY_DEFAULT:
            # SSL habilitado por usuario
            if SSL_CONTEXT and IS_LINUX:
                # Usar contexto personalizado para Linux
                try:
                    adapter = HTTPAdapter()
                    adapter.init_poolmanager(ssl_context=SSL_CONTEXT)
                    self.session.mount('https://', adapter)
                    logger.info("SSL configurado con contexto personalizado para Linux")
                except Exception as e:
                    logger.warning(f"Error configurando SSL personalizado: {e}")
                    self.session.verify = True  # Fallback a verificación estándar
            else:
                # Verificación SSL estándar
                self.session.verify = True
            logger.info(f"SSL verification: ENABLED ({SSL_CONFIG})")
        else:
            # SSL deshabilitado por defecto (compatibilidad universal)
            self.session.verify = False
            logger.info("SSL verification: DISABLED (compatibilidad universal)")
    
    def consultar_deudas(self, cuit: str) -> Dict:
        """
        Consulta deudas en la API del BCRA con múltiples intentos
        
        Args:
            cuit: CUIT limpio (11 dígitos numéricos)
            
        Returns:
            Dict con deudas y resumen
        """
        logger.info(f"Consultando BCRA para CUIT: {cuit[:5]}...")
        
        # Intentar con múltiples URLs
        for url_template in self.API_URLS:
            url = url_template.format(cuit=cuit)
            
            for intento in range(self.MAX_RETRIES):
                try:
                    logger.debug(f"Intento {intento + 1}/{self.MAX_RETRIES} - URL: {url}")
                    
                    response = self.session.get(url, timeout=self.TIMEOUT)
                    
                    if response.status_code == 200:
                        data = response.json()
                        logger.info(f"✅ Datos obtenidos de BCRA - {len(str(data))} caracteres")
                        return self._procesar_respuesta(data, cuit)
                    
                    elif response.status_code == 404:
                        return {"error": "No se encontraron deudas para este CUIT"}
                    
                    elif response.status_code == 400:
                        return {"error": "Formato de CUIT inválido"}
                    
                    elif response.status_code == 429:
                        logger.warning("Rate limit alcanzado, esperando...")
                        time.sleep(2 ** intento)  # Backoff exponencial
                        continue
                    
                    else:
                        logger.warning(f"Error {response.status_code}: {response.text[:200]}")
                        if intento < self.MAX_RETRIES - 1:
                            time.sleep(1)
                            continue
                
                except requests.exceptions.Timeout:
                    logger.warning(f"Timeout en {url}")
                    if intento < self.MAX_RETRIES - 1:
                        time.sleep(2)
                        continue
                
                except requests.exceptions.ConnectionError as e:
                    logger.warning(f"Error de conexión en {url}")
                    if intento < self.MAX_RETRIES - 1:
                        time.sleep(2)
                        continue
                
                except requests.exceptions.SSLError as e:
                    logger.error(f"Error SSL: {e}")
                    
                    # Si SSL está habilitado y falla, sugerir deshabilitarlo
                    if SSL_VERIFY_DEFAULT:
                        return {
                            "error": f"Error de certificados SSL: {str(e)[:200]}...\n\n"
                                    f"Para deshabilitar SSL (compatibilidad universal):\n"
                                    f"export BCRA_SSL_VERIFY=false\n"
                                    f"python run.py\n\n"
                                    f"O para arreglar SSL en Ubuntu:\n"
                                    f"bash scripts/install_ubuntu_ssl.sh"
                        }
                    else:
                        return {
                            "error": f"Error de conexión SSL inesperado: {str(e)[:200]}..."
                        }
                
                except Exception as e:
                    logger.error(f"Error inesperado: {e}")
                    if intento < self.MAX_RETRIES - 1:
                        time.sleep(1)
                        continue
        
        return {"error": "No se pudo conectar con la API del BCRA"}
    
    def _procesar_respuesta(self, data: Dict, cuit: str) -> Dict:
        """Procesa la respuesta de la API del BCRA"""
        try:
            results = data.get('results', {})
            periodos = results.get('periodos', [])
            
            if not periodos:
                return {"error": "No se encontraron deudas para este CUIT"}
            
            deudas = []
            total_deuda = 0
            entidades_unicas = set()
            
            # Procesar todos los períodos y entidades
            for periodo_data in periodos:
                entidades = periodo_data.get('entidades', [])
                
                for entidad_data in entidades:
                    deuda = self._crear_deuda_desde_api(entidad_data, periodo_data)
                    deudas.append(deuda)
                    total_deuda += deuda["montoDeuda"]
                    entidades_unicas.add(deuda["entidadFinanciera"])
            
            logger.info(f"✅ Procesadas {len(deudas)} deudas de {len(entidades_unicas)} entidades")
            
            return {
                "deudas": deudas,
                "resumen": {
                    "totalDeuda": total_deuda,
                    "totalDeudaFormateado": self._formatear_monto(total_deuda),
                    "totalDeudaDetallado": self._formatear_monto_detallado(total_deuda),
                    "cantidadProductos": len(deudas),
                    "bancosAfectados": len(entidades_unicas),
                    "fechaConsulta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                "fuente": "API Directa BCRA - Central de Deudores",
                "cuit_consultado": results.get('identificacion', cuit),
                "denominacion": results.get('denominacion', ''),
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error procesando respuesta BCRA: {e}")
            return {"error": f"Error procesando datos de la API: {str(e)}"}
    
    def _crear_deuda_desde_api(self, entidad_data: Dict, periodo_data: Dict) -> Dict:
        """Crea un objeto de deuda desde los datos de la API"""
        monto = float(entidad_data.get('monto', 0))
        situacion_num = int(entidad_data.get('situacion', 0))
        situacion_info = self._obtener_info_situacion(situacion_num)
        
        return {
            "entidadFinanciera": entidad_data.get('entidad', 'Entidad no especificada'),
            "montoDeuda": monto,
            "montoFormateado": self._formatear_monto(monto),
            "montoDetallado": self._formatear_monto_detallado(monto),
            "situacion": situacion_num,
            "situacionInfo": situacion_info,
            "diasAtraso": int(entidad_data.get('diasAtrasoPago', 0)),
            "tipoProducto": "Financiación",
            "fechaVencimiento": entidad_data.get('fechaSit1', ''),
            "observaciones": "",
            "moneda": "ARS",
            "periodo": periodo_data.get('periodo', ''),
            "refinanciaciones": entidad_data.get('refinanciaciones', False),
            "recategorizacionOblig": entidad_data.get('recategorizacionOblig', False),
            "situacionJuridica": entidad_data.get('situacionJuridica', False),
            "irrecDisposicionTecnica": entidad_data.get('irrecDisposicionTecnica', False),
            "enRevision": entidad_data.get('enRevision', False),
            "procesoJud": entidad_data.get('procesoJud', False)
        }
    
    def procesar_deudas_por_banco(self, deudas: List[Dict]) -> Dict:
        """Agrupa y procesa deudas por banco"""
        deudas_por_banco = {}
        
        for deuda in deudas:
            banco = deuda.get("entidadFinanciera", "Banco no especificado")
            
            if banco not in deudas_por_banco:
                deudas_por_banco[banco] = {
                    "total": 0,
                    "cantidad": 0,
                    "situaciones": [],
                    "situaciones_info": [],
                    "dias_atraso_max": 0,
                    "situacion_principal": deuda.get("situacionInfo", {})
                }
            
            deudas_por_banco[banco]["total"] += deuda.get("montoDeuda", 0)
            deudas_por_banco[banco]["cantidad"] += 1
            deudas_por_banco[banco]["situaciones"].append(deuda.get("situacion", 0))
            deudas_por_banco[banco]["situaciones_info"].append(deuda.get("situacionInfo", {}))
            deudas_por_banco[banco]["dias_atraso_max"] = max(
                deudas_por_banco[banco]["dias_atraso_max"],
                deuda.get("diasAtraso", 0)
            )
            
            # Actualizar situación principal si es más grave
            situacion_actual = deudas_por_banco[banco]["situacion_principal"]
            situacion_nueva = deuda.get("situacionInfo", {})
            if situacion_nueva.get("riesgo") in ["Riesgo alto", "Irrecuperable"] or \
               (situacion_nueva.get("riesgo") == "Riesgo medio" and 
                situacion_actual.get("riesgo") not in ["Riesgo alto", "Irrecuperable"]):
                deudas_por_banco[banco]["situacion_principal"] = situacion_nueva
        
        return deudas_por_banco
    
    def _obtener_info_situacion(self, situacion_num: int) -> Dict:
        """Obtiene información detallada de una situación del BCRA"""
        return self.SITUACIONES.get(situacion_num, {
            "descripcion": "Situación no especificada",
            "riesgo": "No especificado",
            "color": "secondary",
            "icono": "question-circle",
            "explicacion": "No se pudo determinar la situación crediticia."
        })
    
    @staticmethod
    def _formatear_monto(monto: float) -> str:
        """Formatea el monto en miles de pesos con sufijos apropiados"""
        if monto >= 1000:
            return f"${monto/1000:.2f}M"
        else:
            return f"${monto:,.0f}K"
    
    @staticmethod
    def _formatear_monto_detallado(monto: float) -> str:
        """Formatea el monto con separadores de miles y sufijo K"""
        return f"${monto:,.0f}K"

