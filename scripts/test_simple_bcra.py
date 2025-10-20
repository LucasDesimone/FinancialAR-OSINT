#!/usr/bin/env python3
# FinancialAR OSINT
# Copyright (C) 2025 Lucas Desimone
# Licensed under the GNU Affero General Public License v3.0
# See the LICENSE file for details.

"""
Script de prueba simple para la nueva configuración SSL
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

def test_default_config():
    """Prueba la configuración por defecto (sin SSL)"""
    print("="*60)
    print("🧪 PRUEBA: CONFIGURACIÓN POR DEFECTO (SIN SSL)")
    print("="*60)
    
    # Asegurar que no hay variable de entorno SSL
    if 'BCRA_SSL_VERIFY' in os.environ:
        del os.environ['BCRA_SSL_VERIFY']
    
    try:
        from services.bcra_service import BCRAService
        
        print("1️⃣ Creando servicio BCRA...")
        service = BCRAService()
        
        print("2️⃣ Probando consulta...")
        result = service.consultar_deudas("30663288497")
        
        if "error" in result:
            print(f"   ❌ Error: {result['error']}")
            return False
        else:
            print("   ✅ Consulta exitosa!")
            if "resumen" in result:
                resumen = result["resumen"]
                print(f"   📊 Total deuda: {resumen.get('totalDeudaFormateado', 'N/A')}")
                print(f"   📊 Productos: {resumen.get('cantidadProductos', 0)}")
            return True
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_ssl_enabled():
    """Prueba con SSL habilitado"""
    print("\n" + "="*60)
    print("🧪 PRUEBA: CONFIGURACIÓN CON SSL HABILITADO")
    print("="*60)
    
    # Habilitar SSL
    os.environ['BCRA_SSL_VERIFY'] = 'true'
    
    try:
        from services.bcra_service import BCRAService
        
        print("1️⃣ Creando servicio BCRA con SSL...")
        service = BCRAService()
        
        print("2️⃣ Probando consulta...")
        result = service.consultar_deudas("30663288497")
        
        if "error" in result:
            print(f"   ❌ Error: {result['error']}")
            return False
        else:
            print("   ✅ Consulta exitosa!")
            if "resumen" in result:
                resumen = result["resumen"]
                print(f"   📊 Total deuda: {resumen.get('totalDeudaFormateado', 'N/A')}")
                print(f"   📊 Productos: {resumen.get('cantidadProductos', 0)}")
            return True
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    finally:
        # Limpiar variable de entorno
        if 'BCRA_SSL_VERIFY' in os.environ:
            del os.environ['BCRA_SSL_VERIFY']

def main():
    """Función principal"""
    print("🚀 PRUEBA DE CONFIGURACIÓN SSL SIMPLIFICADA")
    
    # Probar configuración por defecto
    default_result = test_default_config()
    
    # Probar configuración con SSL
    ssl_result = test_ssl_enabled()
    
    # Resumen
    print("\n" + "="*60)
    print("📋 RESUMEN DE PRUEBAS")
    print("="*60)
    
    print(f"🔓 Sin SSL (por defecto): {'✅ FUNCIONA' if default_result else '❌ FALLA'}")
    print(f"🔒 Con SSL (opcional): {'✅ FUNCIONA' if ssl_result else '❌ FALLA'}")
    
    print("\n💡 CONFIGURACIÓN RECOMENDADA:")
    print("   • Por defecto: Sin SSL (compatibilidad universal)")
    print("   • Para usuarios avanzados: export BCRA_SSL_VERIFY=true")
    print("   • Para Ubuntu con problemas: bash scripts/install_ubuntu_ssl.sh")

if __name__ == "__main__":
    main()
