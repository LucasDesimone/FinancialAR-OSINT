# 📁 Scripts de FinancialAR OSINT

## 🎯 Scripts disponibles

### **Scripts principales:**
- `test_simple_bcra.py` - Prueba la configuración SSL simplificada
- `test_connection.py` - Diagnóstico general de conectividad
- `crear_indices_db.py` - Crea índices para la base de datos AFIP
- `import_afip_monotributo.py` - Importa datos AFIP a la base de datos

## 🧹 Limpieza realizada

### **Scripts eliminados (ya no necesarios):**
- ❌ `diagnostico_ubuntu_ssl.py` - Diagnóstico complejo SSL
- ❌ `install_ubuntu_ssl.sh` - Instalación automática SSL
- ❌ `test_ubuntu_bcra.py` - Prueba específica Ubuntu
- ❌ `test_no_ssl.py` - Análisis SSL vs No-SSL
- ❌ `analisis_distribuciones.py` - Análisis de compatibilidad

### **Razón de la limpieza:**
La configuración SSL se simplificó para usar **sin verificación SSL por defecto**, eliminando la necesidad de scripts complejos de diagnóstico y configuración específica por distribución.

## 🚀 Uso recomendado

```bash
# Probar configuración
python3 scripts/test_simple_bcra.py

# Diagnóstico general (si hay problemas)
python3 scripts/test_connection.py

# Gestionar base de datos AFIP
python3 scripts/crear_indices_db.py
python3 scripts/import_afip_monotributo.py -i archivo_afip.txt
```

## 📋 Configuración SSL

**Por defecto:** Sin verificación SSL (compatibilidad universal)
- ✅ Funciona en todas las distribuciones
- ✅ Sin configuración adicional necesaria

**Opcional:** Con verificación SSL
- 🔧 Habilitar con: `export BCRA_SSL_VERIFY=true`
- 🔧 Para usuarios que requieran máxima seguridad
