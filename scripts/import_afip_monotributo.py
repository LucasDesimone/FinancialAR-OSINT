#!/usr/bin/env python3
# FinancialAR OSINT
# Copyright (C) 2025 Lucas Desimone
# Licensed under the GNU Affero General Public License v3.0
# See the LICENSE file for details.

"""
Script de importación de base AFIP Monotributo a SQLite
Social Engineering Village 2025

Procesa archivo TXT de AFIP con formato de ancho fijo y genera base SQLite optimizada.
"""

import sqlite3
import os
import sys
from datetime import datetime

# Agregar path del proyecto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def limpiar_texto(texto):
    """Limpia y normaliza texto"""
    return texto.strip().upper()

def parsear_linea_afip(linea):
    """
    Parsea una línea del archivo AFIP con formato de ancho fijo
    
    Formato:
    - CUIT: posición 1-11 (11 chars)
    - DENOMINACION: posición 12-41 (30 chars)
    - IMP_GANANCIAS: posición 42-43 (2 chars)
    - IMP_IVA: posición 44-45 (2 chars)
    - MONOTRIBUTO: posición 46-47 (2 chars)
    - INTEGRANTE_SOC: posición 48 (1 char)
    - EMPLEADOR: posición 49 (1 char)
    - ACTIVIDAD_MONOTRIBUTO: posición 51-52 (2 chars)
    """
    if len(linea) < 52:
        return None
    
    try:
        cuit = linea[0:11].strip()
        denominacion = linea[11:41].strip()
        imp_ganancias = linea[41:43].strip()
        imp_iva = linea[43:45].strip()
        monotributo = linea[45:47].strip()
        integrante_soc = linea[47:48].strip()
        empleador = linea[48:49].strip()
        actividad_monotributo = linea[50:52].strip() if len(linea) >= 52 else ''
        
        # Validar CUIT (debe ser numérico de 11 dígitos)
        if not cuit.isdigit() or len(cuit) != 11:
            return None
        
        # Separar nombre y apellido (heurística simple)
        # Formato común: "APELLIDO NOMBRE" o "SUCESION DE APELLIDO NOMBRE"
        partes = denominacion.split()
        
        if len(partes) >= 2:
            if partes[0] == 'SUCESION' and len(partes) >= 4:
                # "SUCESION DE APELLIDO NOMBRE"
                apellido = ' '.join(partes[2:-1]) if len(partes) > 3 else partes[2]
                nombre = partes[-1]
            else:
                # "APELLIDO NOMBRE" - asumimos primer palabra es apellido
                apellido = partes[0]
                nombre = ' '.join(partes[1:])
        else:
            apellido = denominacion
            nombre = ''
        
        return {
            'cuit': cuit,
            'denominacion': denominacion,
            'apellido': limpiar_texto(apellido),
            'nombre': limpiar_texto(nombre),
            'imp_ganancias': imp_ganancias,
            'imp_iva': imp_iva,
            'monotributo': monotributo,
            'integrante_soc': integrante_soc,
            'empleador': empleador,
            'actividad_monotributo': actividad_monotributo
        }
    except Exception as e:
        print(f"Error parseando línea: {e}")
        return None

def crear_base_datos(db_path):
    """Crea la base de datos SQLite con estructura optimizada"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tabla principal
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contribuyentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cuit TEXT UNIQUE NOT NULL,
            denominacion TEXT NOT NULL,
            apellido TEXT NOT NULL,
            nombre TEXT NOT NULL,
            imp_ganancias TEXT,
            imp_iva TEXT,
            monotributo TEXT,
            integrante_soc TEXT,
            empleador TEXT,
            actividad_monotributo TEXT,
            fecha_importacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Índices para búsqueda rápida
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cuit ON contribuyentes(cuit)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_apellido ON contribuyentes(apellido)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_nombre ON contribuyentes(nombre)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_apellido_nombre ON contribuyentes(apellido, nombre)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_denominacion ON contribuyentes(denominacion)')
    
    conn.commit()
    return conn

def importar_archivo_afip(archivo_txt, db_path):
    """Importa el archivo TXT de AFIP a SQLite"""
    
    print("=" * 80)
    print("🚀 IMPORTACIÓN BASE AFIP MONOTRIBUTO")
    print("=" * 80)
    print(f"📁 Archivo origen: {archivo_txt}")
    print(f"💾 Base de datos: {db_path}")
    print()
    
    # Verificar archivo existe
    if not os.path.exists(archivo_txt):
        print(f"❌ ERROR: Archivo no encontrado: {archivo_txt}")
        return False
    
    # Crear directorio data si no existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Eliminar DB anterior si existe
    if os.path.exists(db_path):
        print("🗑️  Eliminando base de datos anterior...")
        os.remove(db_path)
    
    # Crear base de datos
    print("📊 Creando estructura de base de datos...")
    conn = crear_base_datos(db_path)
    cursor = conn.cursor()
    
    # Contar líneas totales (para progress bar)
    print("📏 Contando registros totales...")
    with open(archivo_txt, 'r', encoding='latin-1') as f:
        total_lineas = sum(1 for _ in f)
    
    print(f"📋 Total de registros a procesar: {total_lineas:,}")
    print()
    
    # Procesar archivo
    print("⚙️  Procesando registros...")
    print("-" * 80)
    
    registros_procesados = 0
    registros_insertados = 0
    registros_error = 0
    
    batch_size = 10000
    batch = []
    
    inicio = datetime.now()
    
    with open(archivo_txt, 'r', encoding='latin-1') as f:
        for i, linea in enumerate(f, 1):
            # Progress bar cada 50k registros
            if i % 50000 == 0:
                porcentaje = (i / total_lineas) * 100
                tiempo_transcurrido = (datetime.now() - inicio).total_seconds()
                velocidad = i / tiempo_transcurrido if tiempo_transcurrido > 0 else 0
                tiempo_restante = (total_lineas - i) / velocidad if velocidad > 0 else 0
                
                print(f"📊 Progreso: {i:,}/{total_lineas:,} ({porcentaje:.1f}%) | "
                      f"Velocidad: {velocidad:,.0f} reg/s | "
                      f"Tiempo restante: {tiempo_restante/60:.1f} min | "
                      f"Insertados: {registros_insertados:,}")
            
            # Parsear línea
            registro = parsear_linea_afip(linea)
            registros_procesados += 1
            
            if registro:
                batch.append((
                    registro['cuit'],
                    registro['denominacion'],
                    registro['apellido'],
                    registro['nombre'],
                    registro['imp_ganancias'],
                    registro['imp_iva'],
                    registro['monotributo'],
                    registro['integrante_soc'],
                    registro['empleador'],
                    registro['actividad_monotributo']
                ))
                
                # Insert batch
                if len(batch) >= batch_size:
                    try:
                        cursor.executemany('''
                            INSERT OR IGNORE INTO contribuyentes 
                            (cuit, denominacion, apellido, nombre, imp_ganancias, imp_iva, 
                             monotributo, integrante_soc, empleador, actividad_monotributo)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', batch)
                        conn.commit()
                        registros_insertados += len(batch)
                        batch = []
                    except Exception as e:
                        print(f"\n⚠️  Error insertando batch: {e}")
                        registros_error += len(batch)
                        batch = []
            else:
                registros_error += 1
    
    # Insertar último batch
    if batch:
        try:
            cursor.executemany('''
                INSERT OR IGNORE INTO contribuyentes 
                (cuit, denominacion, apellido, nombre, imp_ganancias, imp_iva, 
                 monotributo, integrante_soc, empleador, actividad_monotributo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', batch)
            conn.commit()
            registros_insertados += len(batch)
        except Exception as e:
            print(f"\n⚠️  Error insertando último batch: {e}")
            registros_error += len(batch)
    
    # Optimizar base de datos
    print()
    print("🔧 Optimizando base de datos...")
    cursor.execute('VACUUM')
    cursor.execute('ANALYZE')
    conn.commit()
    
    # Estadísticas finales
    tiempo_total = (datetime.now() - inicio).total_seconds()
    
    print()
    print("=" * 80)
    print("✅ IMPORTACIÓN COMPLETADA")
    print("=" * 80)
    print(f"📊 Registros procesados: {registros_procesados:,}")
    print(f"✅ Registros insertados: {registros_insertados:,}")
    print(f"❌ Registros con error: {registros_error:,}")
    print(f"⏱️  Tiempo total: {tiempo_total/60:.2f} minutos")
    print(f"⚡ Velocidad promedio: {registros_procesados/tiempo_total:,.0f} registros/segundo")
    print()
    
    # Tamaño de la base de datos
    db_size = os.path.getsize(db_path) / (1024 * 1024)
    print(f"💾 Tamaño base de datos: {db_size:.2f} MB")
    print()
    
    # Ejemplos de búsqueda
    print("🔍 EJEMPLOS DE BÚSQUEDA:")
    print("-" * 80)
    
    # Buscar por apellido común
    cursor.execute("SELECT COUNT(*) FROM contribuyentes WHERE apellido = 'GONZALEZ'")
    count = cursor.fetchone()[0]
    print(f"📋 Contribuyentes con apellido 'GONZALEZ': {count:,}")
    
    cursor.execute("SELECT COUNT(*) FROM contribuyentes WHERE apellido = 'PEREZ'")
    count = cursor.fetchone()[0]
    print(f"📋 Contribuyentes con apellido 'PEREZ': {count:,}")
    
    # Ejemplo de registro
    cursor.execute("SELECT * FROM contribuyentes LIMIT 1")
    ejemplo = cursor.fetchone()
    if ejemplo:
        print()
        print("📄 EJEMPLO DE REGISTRO:")
        print(f"   CUIT: {ejemplo[1]}")
        print(f"   Denominación: {ejemplo[2]}")
        print(f"   Apellido: {ejemplo[3]}")
        print(f"   Nombre: {ejemplo[4]}")
    
    print()
    print("=" * 80)
    
    conn.close()
    return True

def main():
    """Función principal"""
    import argparse
    
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description='Importar base de datos AFIP de monotributistas a SQLite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  
  # Especificar archivo de origen
  python3 scripts/import_afip_monotributo.py -i /ruta/al/archivo_afip.txt
  
  # Especificar archivo y base de datos personalizada
  python3 scripts/import_afip_monotributo.py -i archivo.txt -o data/custom.db
  
Notas:
  - El archivo TXT debe estar en formato AFIP (ancho fijo)
  - La base de datos se creará automáticamente si no existe
  - El proceso puede tomar varios minutos con archivos grandes
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        help='Ruta al archivo TXT de AFIP (ej: base_afip.txt)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='data/afip_monotributo.db',
        help='Ruta de salida para la base de datos SQLite (default: data/afip_monotributo.db)'
    )
    
    args = parser.parse_args()
    
    # Obtener rutas
    archivo_txt = args.input
    db_path = args.output
    
    # Verificar que el archivo de entrada existe
    if not os.path.exists(archivo_txt):
        print(f"❌ Error: El archivo '{archivo_txt}' no existe")
        print()
        print("💡 Descarga el archivo desde:")
        print("   https://www.afip.gob.ar/genericos/cinscripcion/archivos.asp")
        sys.exit(1)
    
    # Crear directorio de salida si no existe
    output_dir = os.path.dirname(db_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"📁 Directorio creado: {output_dir}")
    
    # Ejecutar importación
    exito = importar_archivo_afip(archivo_txt, db_path)
    
    if exito:
        print()
        print("🎉 ¡Base de datos AFIP lista para usar!")
        print(f"📍 Ubicación: {db_path}")
        print()
        print("🚀 Siguiente paso: Ejecutar la aplicación Flask")
        print("   $ python3 run.py")
    else:
        print("❌ Error en la importación")
        sys.exit(1)

if __name__ == '__main__':
    main()

