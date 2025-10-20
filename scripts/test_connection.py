#!/usr/bin/env python3
# FinancialAR OSINT
# Copyright (C) 2025 Lucas Desimone
# Licensed under the GNU Affero General Public License v3.0
# See the LICENSE file for details.

"""
Script de diagnóstico de conexión a la API del BCRA
Ayuda a identificar problemas de red, firewall, proxy, o SSL en Windows
"""

import requests
import socket
import sys
from urllib.parse import urlparse

print("=" * 80)
print("🔍 DIAGNÓSTICO DE CONEXIÓN - API BCRA")
print("=" * 80)
print()

# URLs a probar
urls = [
    "https://api.bcra.gob.ar/centraldedeudores/v1.0/Deudas/30663288497",
    "https://api.bcra.gob.ar",
    "https://www.google.com",
]

print("1️⃣  Verificando certificados SSL...")

# Verificar truststore (recomendado)
try:
    import truststore
    print(f"   ✅ truststore instalado (usa certificados del sistema)")
    # CRÍTICO: Inyectar truststore en SSL para que requests lo use
    truststore.inject_into_ssl()
    print(f"   ✅ truststore ACTIVADO - requests usará certificados del sistema")
    ssl_method = "truststore"
except ImportError:
    print(f"   ⚠️  truststore NO instalado (se usará certifi)")
    ssl_method = "certifi"

# Verificar certifi (fallback)
try:
    import certifi
    print(f"   ✅ certifi instalado en: {certifi.where()}")
except ImportError:
    print(f"   ❌ certifi NO instalado")
    print(f"   Instala dependencias: pip install -r requirements.txt")
    sys.exit(1)

print()

print("2️⃣  Verificando resolución DNS...")
for url in ["api.bcra.gob.ar", "www.google.com"]:
    try:
        ip = socket.gethostbyname(url)
        print(f"   ✅ {url} → {ip}")
    except Exception as e:
        print(f"   ❌ {url} → Error: {e}")
print()

print("3️⃣  Verificando conectividad TCP...")
for host, port in [("api.bcra.gob.ar", 443), ("www.google.com", 443)]:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            print(f"   ✅ {host}:{port} → Conectado")
        else:
            print(f"   ❌ {host}:{port} → Puerto cerrado o bloqueado")
    except Exception as e:
        print(f"   ❌ {host}:{port} → Error: {e}")
print()

print("4️⃣  Probando requests HTTPS con certificados...")
print()

for url in urls:
    print(f"   Probando: {url}")
    try:
        # Intento 1: Con verificación SSL (certifi)
        print(f"   🔐 Con verificación SSL...", end=" ")
        response = requests.get(
            url, 
            timeout=10,
            verify=certifi.where(),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
        )
        print(f"✅ Status: {response.status_code}")
        
    except requests.exceptions.SSLError as e:
        print(f"❌ Error SSL: {e}")
        
        # Intento 2: Sin verificación SSL (solo diagnóstico)
        print(f"   ⚠️  Probando sin verificación SSL...", end=" ")
        try:
            response = requests.get(url, timeout=10, verify=False)
            print(f"✅ Status: {response.status_code}")
            print(f"   ⚠️  PROBLEMA IDENTIFICADO: Certificados SSL en Windows")
        except Exception as e2:
            print(f"❌ También falla: {e2}")
    
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Error de conexión: {e}")
        print(f"   🔥 POSIBLES CAUSAS:")
        print(f"      • Firewall de Windows bloqueando Python")
        print(f"      • Antivirus bloqueando requests")
        print(f"      • Proxy corporativo requerido")
        print(f"      • VPN o red restrictiva")
        
    except requests.exceptions.Timeout as e:
        print(f"❌ Timeout: {e}")
        print(f"   ⏱️  La conexión es muy lenta o bloqueada")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()

print("=" * 80)
print("📋 RECOMENDACIONES")
print("=" * 80)
print()
print("Si Google funciona pero BCRA no:")
print("  → Firewall de Windows está bloqueando api.bcra.gob.ar")
print("  → Solución: Agregar excepción en el firewall para Python")
print()
print("Si ninguna URL funciona:")
print("  → Problema general de conexión HTTPS desde Python")
print("  → Solución: Configurar proxy o deshabilitar antivirus temporalmente")
print()
print("Si falla con SSL pero funciona sin verificación:")
print("  → Problema de certificados SSL")
if ssl_method == "certifi":
    print("  → Solución RECOMENDADA: pip install --upgrade truststore")
    print("  → Solución alternativa: pip install --upgrade certifi requests urllib3")
else:
    print("  → Solución: pip install --upgrade truststore certifi requests urllib3")
print()
print("Si la conexión TCP falla:")
print("  → Puerto 443 bloqueado por firewall")
print("  → Solución: Verificar configuración de firewall/proxy")
print()
print("💡 NOTA: La aplicación usa 'truststore' que automáticamente utiliza")
print("   los certificados del sistema operativo (Windows/macOS/Linux).")
print("   Esto resuelve la mayoría de problemas SSL en Windows.")
print()
print("=" * 80)

