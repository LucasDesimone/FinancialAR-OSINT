#!/usr/bin/env python3
# FinancialAR OSINT
# Copyright (C) 2025 Lucas Desimone
# Licensed under the GNU Affero General Public License v3.0
# See the LICENSE file for details.

"""
Script para crear índices en la base de datos AFIP
Mejora significativamente la performance de búsquedas

Social Engineering Village 2025
"""

import sqlite3
import os
import sys
import time
from pathlib import Path


def crear_indices(ruta_db: str) -> None:
    """
    Crea índices en la base de datos para mejorar performance
    
    Args:
        ruta_db: Ruta a la base de datos SQLite
    """
    if not os.path.exists(ruta_db):
        print(f"❌ Error: Base de datos no encontrada: {ruta_db}")
        print(f"   Ejecuta primero: python3 scripts/import_afip_monotributo.py")
        sys.exit(1)
    
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║                                                               ║")
    print("║   📊 CREACIÓN DE ÍNDICES EN BASE AFIP                         ║")
    print("║                                                               ║")
    print("╚═══════════════════════════════════════════════════════════════╝\n")
    
    try:
        conn = sqlite3.connect(ruta_db)
        cursor = conn.cursor()
        
        # Verificar si ya existen índices
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='index' AND name LIKE 'idx_%'
        """)
        indices_existentes = cursor.fetchall()
        
        if indices_existentes:
            print(f"⚠️  Se encontraron {len(indices_existentes)} índices existentes:")
            for idx in indices_existentes:
                print(f"   • {idx[0]}")
            
            respuesta = input("\n¿Deseas recrearlos? (s/n): ").lower()
            if respuesta != 's':
                print("❌ Operación cancelada")
                return
            
            # Eliminar índices existentes
            print("\n🗑️  Eliminando índices existentes...")
            for idx in indices_existentes:
                cursor.execute(f"DROP INDEX IF EXISTS {idx[0]}")
            print("✅ Índices eliminados")
        
        # Obtener tamaño de la base antes
        cursor.execute("SELECT COUNT(*) FROM contribuyentes")
        total_registros = cursor.fetchone()[0]
        
        print(f"\n📊 Base de datos:")
        print(f"   • Registros: {total_registros:,}")
        print(f"   • Ubicación: {ruta_db}")
        
        # Crear índices
        indices = [
            ("idx_denominacion", "denominacion"),
            ("idx_apellido", "apellido"),
            ("idx_nombre", "nombre"),
            ("idx_cuit", "cuit")
        ]
        
        print(f"\n🔨 Creando {len(indices)} índices...")
        print("   (Esto puede tomar 30-60 segundos)\n")
        
        for nombre_idx, columna in indices:
            print(f"   • Creando {nombre_idx}...", end=" ", flush=True)
            inicio = time.time()
            
            cursor.execute(f"""
                CREATE INDEX IF NOT EXISTS {nombre_idx} 
                ON contribuyentes({columna})
            """)
            
            duracion = time.time() - inicio
            print(f"✅ ({duracion:.1f}s)")
        
        conn.commit()
        
        # Analizar la base para optimizar índices
        print("\n🔍 Analizando base de datos...")
        cursor.execute("ANALYZE")
        conn.commit()
        print("✅ Análisis completado")
        
        # Verificar índices creados
        cursor.execute("""
            SELECT name, tbl_name FROM sqlite_master 
            WHERE type='index' AND name LIKE 'idx_%'
        """)
        indices_creados = cursor.fetchall()
        
        print(f"\n✅ ÍNDICES CREADOS EXITOSAMENTE")
        print(f"\n📋 Índices activos ({len(indices_creados)}):")
        for nombre, tabla in indices_creados:
            print(f"   • {nombre} → {tabla}")
        
        # Mostrar mejora esperada
        print(f"\n📈 MEJORA ESPERADA:")
        print(f"   • Búsquedas LIKE 'TEXTO%': 20-40x más rápidas ⚡")
        print(f"   • Tiempo de respuesta: ~150-300ms (antes: 7-13s)")
        
        conn.close()
        
        print("\n╔═══════════════════════════════════════════════════════════════╗")
        print("║                                                               ║")
        print("║   ✅ PROCESO COMPLETADO EXITOSAMENTE                          ║")
        print("║                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════╝\n")
        
    except sqlite3.Error as e:
        print(f"\n❌ Error de SQLite: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)


def main():
    """Función principal"""
    # Ruta por defecto
    base_dir = Path(__file__).parent.parent
    ruta_db_default = base_dir / 'data' / 'afip_monotributo.db'
    
    # Usar argumento si se proporciona
    if len(sys.argv) > 1:
        ruta_db = sys.argv[1]
    else:
        ruta_db = str(ruta_db_default)
    
    crear_indices(ruta_db)


if __name__ == '__main__':
    main()

