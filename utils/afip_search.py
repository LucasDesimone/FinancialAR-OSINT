# FinancialAR OSINT
# Copyright (C) 2025 Lucas Desimone
# Licensed under the GNU Affero General Public License v3.0
# See the LICENSE file for details.

"""
Módulo de búsqueda en base AFIP Monotributo
Social Engineering Village 2025

Búsqueda fuzzy y optimizada de contribuyentes por nombre/apellido.
"""

import sqlite3
import os
import re
from difflib import SequenceMatcher

class AFIPSearch:
    """Clase para búsqueda en base AFIP"""
    
    def __init__(self, db_path=None):
        """Inicializa conexión a base de datos"""
        if db_path is None:
            # Ruta por defecto
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, 'data', 'afip_monotributo.db')
        
        self.db_path = db_path
        self.conn = None
        
        # Verificar que existe la base de datos
        if not os.path.exists(db_path):
            raise FileNotFoundError(
                f"Base de datos AFIP no encontrada: {db_path}\n"
                f"Ejecuta primero: python3 scripts/import_afip_monotributo.py"
            )
    
    def conectar(self):
        """Establece conexión a la base de datos"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
    
    def desconectar(self):
        """Cierra conexión a la base de datos"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def normalizar_texto(self, texto):
        """Normaliza texto para búsqueda con sanitización"""
        if not texto:
            return ''
        
        # Limitar longitud
        texto = texto[:100]
        
        # Remover caracteres especiales SQL peligrosos
        texto = re.sub(r'[%_\\]', '', texto)
        
        # Solo permitir alfanuméricos, espacios y caracteres latinos
        texto = re.sub(r'[^\w\s\u00C0-\u017F]', '', texto, flags=re.UNICODE)
        
        return texto.strip().upper()
    
    def similitud_texto(self, texto1, texto2):
        """Calcula similitud entre dos textos (0-1)"""
        return SequenceMatcher(None, texto1, texto2).ratio()
    
    def buscar_por_nombre(self, apellido, nombre='', limite=20):
        """
        Busca contribuyentes por apellido y nombre usando búsqueda inteligente
        en la denominación completa.
        
        Maneja casos complejos:
        - Apellidos compuestos: "DI BLASI"
        - Doble apellido: "GARCIA LOPEZ"
        - Múltiples nombres: "JUAN CARLOS"
        
        Args:
            apellido (str): Apellido o parte del nombre a buscar
            nombre (str): Nombre o parte adicional a buscar (opcional)
            limite (int): Máximo de resultados
        
        Returns:
            list: Lista de diccionarios con resultados ordenados por relevancia
        """
        self.conectar()
        cursor = self.conn.cursor()
        
        apellido_norm = self.normalizar_texto(apellido)
        nombre_norm = self.normalizar_texto(nombre)
        
        # Construir términos de búsqueda
        if nombre_norm:
            # Buscar ambos términos en la denominación
            terminos_busqueda = f"{apellido_norm} {nombre_norm}"
        else:
            terminos_busqueda = apellido_norm
        
        resultados = []
        resultados_dict = {}  # Para evitar duplicados
        
        # ========================================
        # ESTRATEGIA 1: Búsqueda exacta en denominación
        # ========================================
        query = '''
            SELECT * FROM contribuyentes 
            WHERE denominacion LIKE ?
            LIMIT ?
        '''
        cursor.execute(query, (f'%{terminos_busqueda}%', limite * 3))
        rows = cursor.fetchall()
        
        for row in rows:
            denominacion = row['denominacion']
            cuit = row['cuit']
            
            # Calcular score basado en similitud con denominación completa
            score = self.similitud_texto(terminos_busqueda, denominacion) * 100
            
            # Bonus si empieza con el término buscado
            if denominacion.startswith(apellido_norm):
                score += 10
            
            # Bonus si contiene ambos términos en orden
            if nombre_norm and apellido_norm in denominacion and nombre_norm in denominacion:
                idx_apellido = denominacion.find(apellido_norm)
                idx_nombre = denominacion.find(nombre_norm)
                if idx_apellido < idx_nombre:
                    score += 15
            
            # ========================================
            # LÓGICA ESTRICTA PARA COINCIDENCIA EXACTA
            # ========================================
            # Solo es 100% si:
            # 1. Los términos buscados están en la denominación
            # 2. La diferencia de longitud es mínima (máx 3 caracteres)
            #    Esto permite variaciones menores pero no nombres adicionales
            
            if terminos_busqueda in denominacion:
                # Calcular diferencia de longitud
                diff_longitud = abs(len(denominacion) - len(terminos_busqueda))
                
                # Coincidencia exacta: diferencia mínima (ej: espacios extra)
                if diff_longitud <= 3:
                    score = 100
                # Alta similitud: contiene los términos pero tiene palabras adicionales
                elif diff_longitud <= 15:
                    score = 98
                else:
                    score = 95
            # Alta similitud: muy similar pero no contiene términos exactos
            elif score >= 90:
                score = min(score, 97)
            # Limitar score a 100
            else:
                score = min(score, 100)
            
            if cuit not in resultados_dict or resultados_dict[cuit]['match_score'] < score:
                resultados_dict[cuit] = {
                    'cuit': cuit,
                    'denominacion': denominacion,
                    'apellido': row['apellido'],
                    'nombre': row['nombre'],
                    'monotributo': row['monotributo'],
                    'imp_iva': row['imp_iva'],
                    'imp_ganancias': row['imp_ganancias'],
                    'integrante_soc': row['integrante_soc'],
                    'empleador': row['empleador'],
                    'actividad_monotributo': row['actividad_monotributo'],
                    'match_score': round(score, 1)
                }
        
        # ========================================
        # ESTRATEGIA 2: Búsqueda por palabras individuales
        # ========================================
        # Buscar cada palabra del apellido por separado (para apellidos compuestos)
        palabras = apellido_norm.split()
        if nombre_norm:
            palabras.extend(nombre_norm.split())
        
        for palabra in palabras:
            if len(palabra) < 3:  # Ignorar palabras muy cortas
                continue
            
            query = '''
                SELECT * FROM contribuyentes 
                WHERE denominacion LIKE ?
                LIMIT ?
            '''
            cursor.execute(query, (f'%{palabra}%', limite * 2))
            rows = cursor.fetchall()
            
            for row in rows:
                cuit = row['cuit']
                denominacion = row['denominacion']
                
                # Calcular cuántas palabras coinciden
                palabras_encontradas = sum(1 for p in palabras if p in denominacion)
                score = (palabras_encontradas / len(palabras)) * 80
                
                # Bonus por similitud general
                score += self.similitud_texto(terminos_busqueda, denominacion) * 20
                
                # Limitar score a 100
                score = min(score, 100)
                
                if cuit not in resultados_dict or resultados_dict[cuit]['match_score'] < score:
                    resultados_dict[cuit] = {
                        'cuit': cuit,
                        'denominacion': denominacion,
                        'apellido': row['apellido'],
                        'nombre': row['nombre'],
                        'monotributo': row['monotributo'],
                        'imp_iva': row['imp_iva'],
                        'imp_ganancias': row['imp_ganancias'],
                        'integrante_soc': row['integrante_soc'],
                        'empleador': row['empleador'],
                        'actividad_monotributo': row['actividad_monotributo'],
                        'match_score': round(score, 1)
                    }
        
        # ========================================
        # ESTRATEGIA 3: Búsqueda en campos apellido/nombre (fallback)
        # ========================================
        if len(resultados_dict) < limite:
            if nombre_norm:
                query = '''
                    SELECT * FROM contribuyentes 
                    WHERE apellido LIKE ? OR nombre LIKE ? OR apellido LIKE ? OR nombre LIKE ?
                    LIMIT ?
                '''
                cursor.execute(query, (
                    f'%{apellido_norm}%', f'%{apellido_norm}%',
                    f'%{nombre_norm}%', f'%{nombre_norm}%',
                    limite * 2
                ))
            else:
                query = '''
                    SELECT * FROM contribuyentes 
                    WHERE apellido LIKE ? OR nombre LIKE ?
                    LIMIT ?
                '''
                cursor.execute(query, (f'%{apellido_norm}%', f'%{apellido_norm}%', limite * 2))
            
            rows = cursor.fetchall()
            
            for row in rows:
                cuit = row['cuit']
                if cuit in resultados_dict:
                    continue
                
                denominacion = row['denominacion']
                score = self.similitud_texto(terminos_busqueda, denominacion) * 70
                
                resultados_dict[cuit] = {
                    'cuit': cuit,
                    'denominacion': denominacion,
                    'apellido': row['apellido'],
                    'nombre': row['nombre'],
                    'monotributo': row['monotributo'],
                    'imp_iva': row['imp_iva'],
                    'imp_ganancias': row['imp_ganancias'],
                    'integrante_soc': row['integrante_soc'],
                    'empleador': row['empleador'],
                    'actividad_monotributo': row['actividad_monotributo'],
                    'match_score': round(score, 1)
                }
        
        # Convertir dict a lista y ordenar por score
        resultados = list(resultados_dict.values())
        resultados.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Limitar resultados
        return resultados[:limite]
    
    def buscar_por_cuit(self, cuit):
        """
        Busca contribuyente por CUIT exacto
        
        Args:
            cuit (str): CUIT a buscar
        
        Returns:
            dict: Datos del contribuyente o None
        """
        self.conectar()
        cursor = self.conn.cursor()
        
        # Limpiar CUIT (solo números)
        cuit_limpio = ''.join(filter(str.isdigit, cuit))
        
        query = 'SELECT * FROM contribuyentes WHERE cuit = ?'
        cursor.execute(query, (cuit_limpio,))
        
        row = cursor.fetchone()
        
        if row:
            return {
                'cuit': row['cuit'],
                'denominacion': row['denominacion'],
                'apellido': row['apellido'],
                'nombre': row['nombre'],
                'monotributo': row['monotributo'],
                'imp_iva': row['imp_iva'],
                'imp_ganancias': row['imp_ganancias']
            }
        
        return None
    
    def estadisticas(self):
        """Obtiene estadísticas de la base de datos"""
        self.conectar()
        cursor = self.conn.cursor()
        
        # Total de registros
        cursor.execute('SELECT COUNT(*) FROM contribuyentes')
        total = cursor.fetchone()[0]
        
        # Monotributistas
        cursor.execute("SELECT COUNT(*) FROM contribuyentes WHERE monotributo != 'NI'")
        monotributistas = cursor.fetchone()[0]
        
        # Con IVA
        cursor.execute("SELECT COUNT(*) FROM contribuyentes WHERE imp_iva != 'NI'")
        con_iva = cursor.fetchone()[0]
        
        # Con Ganancias
        cursor.execute("SELECT COUNT(*) FROM contribuyentes WHERE imp_ganancias != 'NI'")
        con_ganancias = cursor.fetchone()[0]
        
        return {
            'total_registros': total,
            'monotributistas': monotributistas,
            'responsables_iva': con_iva,
            'ganancias': con_ganancias
        }
    
    def __enter__(self):
        """Context manager entry"""
        self.conectar()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.desconectar()


# Función helper para uso directo
def buscar_contribuyente(apellido, nombre='', limite=20):
    """
    Función helper para búsqueda rápida
    
    Args:
        apellido (str): Apellido a buscar
        nombre (str): Nombre a buscar (opcional)
        limite (int): Máximo de resultados
    
    Returns:
        list: Lista de resultados
    """
    with AFIPSearch() as search:
        return search.buscar_por_nombre(apellido, nombre, limite)


def buscar_por_cuit(cuit):
    """
    Función helper para búsqueda por CUIT
    
    Args:
        cuit (str): CUIT a buscar
    
    Returns:
        dict: Datos del contribuyente o None
    """
    with AFIPSearch() as search:
        return search.buscar_por_cuit(cuit)


# Test rápido
if __name__ == '__main__':
    print("🔍 Test de búsqueda AFIP")
    print("=" * 60)
    
    # Test búsqueda por apellido
    print("\n📋 Buscando 'GONZALEZ JUAN'...")
    resultados = buscar_contribuyente('GONZALEZ', 'JUAN', limite=5)
    
    if resultados:
        print(f"✅ Encontrados {len(resultados)} resultados:")
        for i, r in enumerate(resultados, 1):
            print(f"\n{i}. {r['denominacion']}")
            print(f"   CUIT: {r['cuit']}")
            print(f"   Match: {r['match_score']}%")
    else:
        print("❌ No se encontraron resultados")
    
    # Estadísticas
    print("\n" + "=" * 60)
    print("📊 ESTADÍSTICAS DE LA BASE:")
    with AFIPSearch() as search:
        stats = search.estadisticas()
        print(f"   Total registros: {stats['total_registros']:,}")
        print(f"   Monotributistas: {stats['monotributistas']:,}")
        print(f"   Responsables IVA: {stats['responsables_iva']:,}")
        print(f"   Ganancias: {stats['ganancias']:,}")

