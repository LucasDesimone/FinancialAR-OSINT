# FinancialAR OSINT
# Copyright (C) 2025 Lucas Desimone
# Licensed under the GNU Affero General Public License v3.0
# See the LICENSE file for details.

"""
Validadores y sanitizadores de entrada
Social Engineering Village 2025
"""
import re
from typing import Optional

class CUITValidator:
    """Validador de CUIT con sanitización"""
    
    PREFIJOS_VALIDOS = ['20', '23', '24', '27', '30', '33', '34']
    
    @staticmethod
    def limpiar(cuit: str) -> str:
        """Limpia CUIT removiendo caracteres no numéricos"""
        return re.sub(r'[^\d]', '', cuit)
    
    @classmethod
    def validar(cls, cuit: str) -> bool:
        """Valida formato de CUIT argentino"""
        cuit_limpio = cls.limpiar(cuit)
        
        # Verificar longitud
        if len(cuit_limpio) != 11:
            raise ValueError(f"CUIT debe tener 11 dígitos, recibido: {len(cuit_limpio)}")
        
        # Verificar prefijo válido
        if cuit_limpio[:2] not in cls.PREFIJOS_VALIDOS:
            raise ValueError(f"Prefijo de CUIT inválido: {cuit_limpio[:2]}")
        
        return True
    
    @classmethod
    def formatear(cls, cuit: str) -> str:
        """Formatea CUIT como XX-XXXXXXXX-X"""
        cuit_limpio = cls.limpiar(cuit)
        if len(cuit_limpio) == 11:
            return f"{cuit_limpio[:2]}-{cuit_limpio[2:10]}-{cuit_limpio[10]}"
        return cuit_limpio


class TextoSanitizer:
    """Sanitiza texto de búsquedas SQL"""
    
    @staticmethod
    def sanitizar_busqueda(texto: str, max_length: int = 100) -> str:
        """Sanitiza texto para búsquedas SQL"""
        if not texto:
            return ''
        
        # Limitar longitud
        texto = texto[:max_length]
        
        # Remover caracteres especiales SQL peligrosos
        texto = re.sub(r'[%_\\]', '', texto)
        
        # Solo permitir alfanuméricos, espacios y caracteres latinos (acentos)
        texto = re.sub(r'[^\w\s\u00C0-\u017F]', '', texto, flags=re.UNICODE)
        
        return texto.strip().upper()

