# FinancialAR OSINT
# Copyright (C) 2025 Lucas Desimone
# Licensed under the GNU Affero General Public License v3.0
# See the LICENSE file for details.

"""
Servicio para búsquedas en base AFIP
Encapsula lógica de negocio de búsqueda de contribuyentes
"""
from typing import List, Dict
from utils.afip_search import AFIPSearch
import logging

logger = logging.getLogger(__name__)


class AFIPService:
    """Servicio para búsquedas en base AFIP de monotributistas"""
    
    def __init__(self, db_path: str = None):
        """
        Inicializa el servicio AFIP
        
        Args:
            db_path: Ruta a la base de datos AFIP (opcional)
        """
        self.db_path = db_path
    
    def buscar_contribuyentes(self, apellido: str, nombre: str = '', limite: int = 20) -> Dict:
        """
        Busca contribuyentes por nombre y apellido
        
        Args:
            apellido: Apellido a buscar
            nombre: Nombre a buscar (opcional)
            limite: Máximo de resultados
            
        Returns:
            Dict con resultados y metadata
        """
        logger.info(f"Buscando contribuyentes: {apellido} {nombre}")
        
        try:
            with AFIPSearch(db_path=self.db_path) as search:
                resultados = search.buscar_por_nombre(apellido, nombre, limite)
            
            logger.info(f"✅ Encontrados {len(resultados)} contribuyentes")
            
            return {
                'success': True,
                'resultados': resultados,
                'total': len(resultados),
                'query': {
                    'apellido': apellido,
                    'nombre': nombre
                }
            }
        
        except FileNotFoundError as e:
            logger.error(f"Base de datos AFIP no encontrada: {e}")
            return {
                'success': False,
                'error': 'Base de datos AFIP no disponible. Ejecute el script de importación primero.',
                'instrucciones': 'python3 scripts/import_afip_monotributo.py'
            }
        
        except Exception as e:
            logger.error(f"Error en búsqueda AFIP: {e}")
            return {
                'success': False,
                'error': f'Error en la búsqueda: {str(e)}'
            }
    
    def buscar_por_cuit(self, cuit: str) -> Dict:
        """
        Busca un contribuyente por CUIT exacto
        
        Args:
            cuit: CUIT a buscar
            
        Returns:
            Dict con datos del contribuyente o None
        """
        logger.info(f"Buscando por CUIT: {cuit[:5]}...")
        
        try:
            with AFIPSearch(db_path=self.db_path) as search:
                resultado = search.buscar_por_cuit(cuit)
            
            if resultado:
                logger.info(f"✅ Contribuyente encontrado: {resultado.get('denominacion')}")
                return {
                    'success': True,
                    'resultado': resultado
                }
            else:
                logger.info("No se encontró contribuyente con ese CUIT")
                return {
                    'success': False,
                    'error': 'No se encontró contribuyente con ese CUIT'
                }
        
        except Exception as e:
            logger.error(f"Error buscando por CUIT: {e}")
            return {
                'success': False,
                'error': f'Error en la búsqueda: {str(e)}'
            }
    
    def obtener_estadisticas(self) -> Dict:
        """
        Obtiene estadísticas de la base AFIP
        
        Returns:
            Dict con estadísticas
        """
        logger.info("Obteniendo estadísticas AFIP")
        
        try:
            with AFIPSearch(db_path=self.db_path) as search:
                stats = search.estadisticas()
            
            logger.info(f"✅ Estadísticas obtenidas: {stats.get('total_registros', 0):,} registros")
            
            return {
                'success': True,
                'estadisticas': stats
            }
        
        except FileNotFoundError:
            logger.error("Base de datos AFIP no disponible")
            return {
                'success': False,
                'error': 'Base de datos AFIP no disponible'
            }
        
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {
                'success': False,
                'error': str(e)
            }

