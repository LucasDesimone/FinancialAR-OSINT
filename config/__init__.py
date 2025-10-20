# FinancialAR OSINT
# Copyright (C) 2025 Lucas Desimone
# Licensed under the GNU Affero General Public License v3.0
# See the LICENSE file for details.

"""
Paquete de configuración
Social Engineering Village 2025
"""

from .bancos_config import (
    BANCOS_CONFIG,
    LOGOS_BANCOS,
    COLORES_BANCOS,
    NOMBRES_BANCOS,
    get_banco_info,
    normalizar_nombre_banco,
    listar_bancos,
    get_email_fake_banco,
    get_telefono_fake_banco,
    get_color_banco,
    get_logo_banco
)

__all__ = [
    'BANCOS_CONFIG',
    'LOGOS_BANCOS',
    'COLORES_BANCOS',
    'NOMBRES_BANCOS',
    'get_banco_info',
    'normalizar_nombre_banco',
    'listar_bancos',
    'get_email_fake_banco',
    'get_telefono_fake_banco',
    'get_color_banco',
    'get_logo_banco'
]

