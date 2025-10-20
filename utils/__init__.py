# FinancialAR OSINT
# Copyright (C) 2025 Lucas Desimone
# Licensed under the GNU Affero General Public License v3.0
# See the LICENSE file for details.

"""
Utilidades para el sistema de consulta de deudas BCRA
Social Engineering Village 2025
"""

from .afip_search import AFIPSearch, buscar_contribuyente, buscar_por_cuit

__all__ = ['AFIPSearch', 'buscar_contribuyente', 'buscar_por_cuit']

