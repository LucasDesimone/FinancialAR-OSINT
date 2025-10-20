# 🔍 FinancialAR OSINT

**Herramienta de Inteligencia Financiera y Concientización sobre Ingeniería Social**

Desarrollado para **Social Engineering Village 2025** - Ekoparty Security Conference

---

## 📋 Descripción

FinancialAR OSINT es una herramienta educativa que permite:

- ✅ **Consultar deudas bancarias** del BCRA (Banco Central de la República Argentina)
- ✅ **Buscar personas por nombre** en la base de datos AFIP de monotributistas
- ✅ **Generar emails de phishing educativos** para concientización
- ✅ **Crear landing pages de phishing** simuladas de bancos argentinos
- ✅ **Demostrar técnicas de OSINT** aplicadas al ámbito financiero

---

## 🚀 Instalación

### 1. Requisitos Previos

- **Python 3.8+**
- **pip** (gestor de paquetes de Python)
- **Git** (opcional, para clonar el repositorio)

### 2. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/FinancialAR-OSINT.git
cd FinancialAR-OSINT
```

### 3. Crear Entorno Virtual (Recomendado)

```bash
python3 -m venv .venv
source .venv/bin/activate  # En Linux/Mac
# o
.venv\Scripts\activate  # En Windows
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

---

## 🗄️ Configuración de la Base de Datos AFIP

Para utilizar la funcionalidad de búsqueda por nombre, necesitas importar la base de datos de monotributistas de AFIP.

### 1. Descargar el Archivo AFIP

Descarga el archivo de monotributistas desde:
👉 https://www.afip.gob.ar/genericos/cInscripcion/archivoCompleto.asp

Busca el archivo: **"Padrón de Monotributistas"** (formato TXT)

### 2. Importar a la Base de Datos

```bash
python3 scripts/import_afip_monotributo.py -i /ruta/al/archivo_afip.txt
```

**Ejemplo:**
```bash
python3 scripts/import_afip_monotributo.py -i ~/Downloads/base_afip.txt
```

**Opciones disponibles:**

```bash
# Especificar archivo de entrada y salida personalizada
python3 scripts/import_afip_monotributo.py -i archivo.txt -o data/custom.db

# Ver ayuda
python3 scripts/import_afip_monotributo.py --help
```

**Notas:**
- ⏱️ El proceso puede tomar varios minutos (archivo de ~6 millones de registros)
- 💾 La base de datos se creará en `data/afip_monotributo.db` por defecto
- 📁 El directorio `data/` se creará automáticamente si no existe
- 📊 **Los índices se crean automáticamente** para optimizar búsquedas (no es necesario ejecutar `crear_indices_db.py`)

---

## 🎯 Uso

### Iniciar la Aplicación

```bash
python3 run.py
```

La aplicación estará disponible en:
- **URL Local:** http://localhost:5050
- **URL Red:** http://[tu-ip-local]:5050

### Banner de Inicio

Al ejecutar `run.py`, verás un banner ASCII profesional:

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                    FINANCIAL AR OSINT (ASCII Art)                         ║
╚═══════════════════════════════════════════════════════════════════════════╝

🔍 Herramienta de Inteligencia Financiera y Concientización OSINT
📍 Social Engineering Village 2025 - Ekoparty Security Conference
💻 Desarrollado por Lucas Desimone
```

---

## 🛠️ Funcionalidades

### 1. Consulta de Deudas BCRA

- Busca por **CUIT/CUIL** (formato: XX-XXXXXXXX-X)
- Obtiene datos **reales** de la API oficial del BCRA
- Muestra deudas por entidad financiera
- Visualiza situación crediticia completa

### 2. Búsqueda por Nombre (AFIP)

- Busca personas en la base de datos de monotributistas
- Algoritmo de **fuzzy matching** para coincidencias parciales
- Muestra información fiscal: Monotributo, IVA, Ganancias, Actividad
- Categorías de similitud: Exacta, Alta, Moderada, Baja, Parcial

### 3. Generación de Emails de Phishing Educativos

- Templates personalizados por banco
- **13 bancos argentinos** soportados:
  - Galicia, BBVA, Provincia, Santander, ICBC
  - Supervielle, Cencosud, Mercado Pago, Nación
  - Hipotecario, Credicoop, Comafi, Macro, Tarjeta Naranja
- Contenido dinámico (nombre, banco, monto de deuda)
- Visualización en nueva pestaña

### 4. Landing Pages de Phishing Simuladas

- Páginas de login realistas por banco
- Logos y colores corporativos auténticos
- Campos de login específicos por entidad
- **Propósito educativo** para demostrar riesgos

---

## 📁 Estructura del Proyecto

```
FinancialAR-OSINT/
├── app.py                      # Aplicación Flask principal (controllers)
├── run.py                      # Script de inicio con banner ASCII
├── config.py                   # Configuración de la aplicación
├── requirements.txt            # Dependencias de Python
├── README.md                   # Este archivo
│
├── config/                     # Configuración centralizada
│   ├── __init__.py
│   ├── bancos_config.py       # Configuración de bancos (single source of truth)
│   └── bancos_nombres.py      # Mapeo de nombres de bancos
│
├── services/                   # Capa de servicios (business logic)
│   ├── __init__.py
│   ├── bcra_service.py        # Servicio de consultas BCRA (SSL simplificado)
│   ├── afip_service.py        # Servicio de búsqueda AFIP
│   └── phishing_service.py    # Servicio de generación de phishing
│
├── utils/                      # Utilidades y validadores
│   ├── __init__.py
│   ├── afip_search.py         # Motor de búsqueda AFIP con fuzzy matching
│   └── validators.py          # Validación y sanitización de inputs
│
├── data/                       # Base de datos (creada automáticamente)
│   └── afip_monotributo.db    # Base de datos AFIP (después de importar)
│
├── scripts/                    # Scripts de utilidad
│   ├── __init__.py
│   ├── import_afip_monotributo.py  # Importador de base AFIP (crea índices automáticamente)
│   ├── crear_indices_db.py    # Utilidad de mantenimiento (opcional, para recrear índices)
│   ├── test_simple_bcra.py    # Prueba de configuración SSL simplificada
│   ├── test_connection.py     # Diagnóstico general de conectividad
│   └── README_scripts.md      # Documentación de scripts disponibles
│
├── templates/                  # Templates HTML
│   ├── index.html             # Página principal
│   ├── landing_phishing.html  # Template de landing pages
│   └── email_templates.py     # Generador de emails de phishing
│
└── static/                     # Archivos estáticos
    ├── css/
    │   └── style.css          # Estilos modernos (dark theme)
    ├── js/
    │   └── app.js             # JavaScript frontend (modularizado)
    └── images/                # Logos de bancos y assets
        ├── banner_financialAR_osint.png
        ├── banco_galicia.png
        ├── banco_bbva.png
        ├── banco_provincia.png
        └── ... (13 bancos más)
```

### 🏗️ Arquitectura

La aplicación sigue una **arquitectura en capas** con separación de responsabilidades:

1. **Controllers** (`app.py`): Manejo de rutas, validación de requests y responses
2. **Services** (`services/`): Lógica de negocio centralizada
   - `BCRAService`: Consultas a la API del BCRA y procesamiento de deudas
   - `AFIPService`: Búsqueda en base de datos AFIP con fuzzy matching
   - `PhishingService`: Generación de contenido de phishing educativo
3. **Utils** (`utils/`): Validadores, sanitizadores y utilidades compartidas
4. **Config** (`config/`): Configuración centralizada (single source of truth)

---

## 🔒 Consideraciones de Seguridad

### ⚠️ Advertencias Importantes

1. **Propósito Educativo:** Esta herramienta es **solo para concientización** sobre ingeniería social
2. **Uso Responsable:** NO usar para actividades maliciosas o ilegales
3. **Datos Reales:** La herramienta consulta APIs reales del BCRA e información de AFIP
4. **Privacidad:** Respetar la privacidad de las personas consultadas
5. **Entorno de Desarrollo:** El servidor Flask es para desarrollo, NO para producción

## 🎨 Personalización

### Agregar Nuevos Bancos

1. **Agregar logo:** Coloca el logo en `static/images/banco_nombre.png`
2. **Configurar banco:** Edita `config/bancos_config.py`:
   ```python
   BANCOS_CONFIG = {
       'NUEVO BANCO': {
           'nombre_completo': 'Banco Nuevo',
           'nombre_oficial': 'Banco Nuevo S.A.',
           'logo': 'banco_nuevo.png',
           'color': '#hexcolor',
           'email_fake': 'alertas@banco-nuevo.com',
           'telefono_fake': '+54 11 XXXX-XXXX'
       },
       # ...
   }
   ```
3. **Configurar campos de login:** Edita `CAMPOS_LOGIN_BANCOS` en `templates/email_templates.py`
4. **Configurar template de email:** Agrega el template correspondiente en `email_templates.py`

### Modificar Estilos

- **CSS principal:** `static/css/style.css`
- **Colores del tema:** Variables CSS en `:root` (líneas 6-54)
- **Banner:** Edita la imagen `static/images/banner_financialAR_osint.png`
- **Banner ASCII:** `run.py` función `print_banner()`

### Arquitectura de Configuración

La aplicación usa **Single Source of Truth** para configuración:
- **Bancos:** `config/bancos_config.py` (configuración centralizada)
- **Servicios:** Importan desde `config/` para mantener consistencia
- **Frontend:** Obtiene configuración desde backend (no hardcodeado)

---

### Error: "No se pudo conectar con la API del BCRA" (Windows)

Este error suele ocurrir en **Windows** por varios motivos:

#### 🔍 Paso 1: Diagnóstico

Ejecuta el script de diagnóstico para identificar el problema:

```bash
python scripts/test_connection.py
```

Este script verificará:
- ✅ Certificados SSL
- ✅ Resolución DNS
- ✅ Conectividad TCP
- ✅ Conexión HTTPS

#### 🔧 Soluciones según el problema identificado

**A) Error de certificados SSL (RECOMENDADO):**

La aplicación usa **truststore** que automáticamente utiliza los certificados del sistema operativo:
- 🪟 **Windows:** Almacén de certificados del sistema
- 🍎 **macOS:** Keychain
- 🐧 **Linux:** /etc/ssl/certs

```bash
# Actualizar todas las dependencias SSL
pip install --upgrade truststore certifi requests urllib3

# Reiniciar la aplicación
python run.py
```

**Nota:** `truststore` es multiplataforma y funciona automáticamente en Windows/macOS/Linux sin configuración adicional.

**B) Firewall de Windows bloqueando Python:**
1. Abrir "Firewall de Windows Defender"
2. Click en "Permitir una aplicación a través del firewall"
3. Click en "Cambiar configuración" → "Permitir otra aplicación"
4. Buscar `python.exe` (generalmente en `C:\Python3x\python.exe`)
5. Marcar "Privada" y "Pública" → Agregar

**C) Antivirus bloqueando requests:**
- Agregar excepción para `python.exe` en el antivirus
- Agregar excepción para la carpeta del proyecto

**D) Proxy corporativo:**
```bash
# Configurar proxy en Windows (cmd)
set HTTP_PROXY=http://proxy:puerto
set HTTPS_PROXY=http://proxy:puerto
python run.py
```

**E) Reinstalar dependencias completas:**
```bash
pip uninstall truststore certifi requests urllib3
pip install -r requirements.txt
```

**Nota técnica:** La aplicación intenta usar `truststore` primero (certificados del sistema) y si no está disponible, hace fallback a `certifi` (certificados empaquetados).

### Error: "No se pudo conectar con la API del BCRA"

Este error puede ocurrir por problemas de certificados SSL, especialmente en Ubuntu/Linux.

#### 🔧 Solución simple (RECOMENDADO)

La aplicación está configurada por defecto **SIN verificación SSL** para máxima compatibilidad:

```bash
# La aplicación funciona automáticamente sin configuración adicional
python run.py
```

#### 🔧 Solución con SSL (opcional)

Si necesitas verificación SSL completa:

```bash
# Habilitar SSL (solo si es necesario)
export BCRA_SSL_VERIFY=true
python run.py
```

#### 🔧 Para problemas SSL específicos

Si tienes problemas con SSL en tu distribución:

```bash
# Solución manual para Ubuntu/Debian
sudo apt update && sudo apt install ca-certificates
sudo update-ca-certificates
pip install --upgrade truststore certifi requests urllib3

# O habilitar SSL si es necesario
export BCRA_SSL_VERIFY=true
python run.py
```

#### 🧪 Prueba de configuración

Verifica que todo funciona correctamente:

```bash
python3 scripts/test_simple_bcra.py
```

#### 📋 Configuración SSL

**Por defecto:** Sin verificación SSL (compatibilidad universal)
- ✅ Funciona en todas las distribuciones
- ✅ Instalación plug-and-play
- ✅ Sin problemas de certificados

**Opcional:** Con verificación SSL
- 🔒 Máxima seguridad
- ⚠️ Puede requerir configuración adicional
- 🔧 Habilitar con `export BCRA_SSL_VERIFY=true`

#### 🚨 Si persiste el problema

1. **Verificar conectividad:**
   ```bash
   curl -I https://api.bcra.gob.ar
   ```

2. **Verificar firewall:**
   ```bash
   sudo ufw status
   sudo ufw allow out 443
   ```

3. **Probar con VPN temporalmente** para descartar bloqueos de red

**Nota técnica:** La configuración por defecto prioriza la compatibilidad universal. Los datos siguen viajando cifrados (HTTPS), solo se deshabilita la verificación de identidad del servidor.

---

## 🔧 Configuración SSL Simplificada

### **Configuración por defecto:**
- ✅ **Sin verificación SSL** (compatibilidad universal)
- ✅ **Funciona en todas las distribuciones** (Ubuntu, Debian, CentOS, Arch, etc.)
- ✅ **Instalación plug-and-play** (sin configuración adicional)
- ✅ **Datos cifrados** (HTTPS sigue activo)

### **Configuración opcional:**
- 🔧 **Con verificación SSL:** `export BCRA_SSL_VERIFY=true`
- 🔧 **Para usuarios avanzados** que requieran máxima seguridad
- 🔧 **Para entornos corporativos** con políticas de seguridad estrictas

### **Scripts de prueba:**
```bash
# Probar configuración actual
python3 scripts/test_simple_bcra.py

# Diagnóstico general (si hay problemas)
python3 scripts/test_connection.py
```

### Base de datos AFIP no funciona

```bash
# Verificar que existe
ls -lh data/afip_monotributo.db

# Reimportar si es necesario
python3 scripts/import_afip_monotributo.py -i archivo_afip.txt
```

### Búsquedas AFIP lentas

**Los índices se crean automáticamente** durante la importación. Si las búsquedas son lentas, puede ser porque:

1. La base de datos fue creada con una versión antigua del script sin índices
2. Los índices se corrompieron

**Solución:**
```bash
# Recrear índices manualmente
python3 scripts/crear_indices_db.py

# O reimportar la base de datos completa
python3 scripts/import_afip_monotributo.py -i archivo_afip.txt
```

---

## 📚 Recursos Adicionales

- **API BCRA:** https://api.bcra.gob.ar/
- **AFIP Monotributo:** https://www.afip.gob.ar/monotributo/
- **Social Engineering Village:** [Ekoparty](https://www.ekoparty.org/)

---

## 👨‍💻 Autor

**Lucas Desimone**

Desarrollado para **Social Engineering Village 2025** - Ekoparty Security Conference

---

## 📄 Licencia

Este proyecto está licenciado bajo la **GNU Affero General Public License v3.0 (AGPL-3.0)**.

Esta licencia copyleft garantiza que:
- ✅ Puedes usar, modificar y distribuir el código libremente
- ✅ Cualquier modificación debe ser compartida bajo la misma licencia
- ✅ Si usas este software en un servidor web, debes proporcionar el código fuente a los usuarios
- ✅ Protege la libertad del software y sus derivados

Para más detalles, consulta el archivo [LICENSE](LICENSE) en la raíz del repositorio.

**Uso Responsable:** Esta herramienta es solo para fines educativos y de concientización sobre seguridad. El autor no se hace responsable del uso indebido de esta herramienta.


---

## 🚀 Mejoras Técnicas Recientes

### Refactorización de Arquitectura (2025)

- ✅ **Capa de Servicios:** Separación completa de lógica de negocio
- ✅ **Single Source of Truth:** Configuración centralizada de bancos
- ✅ **Input Validation:** Validadores y sanitizadores robustos
- ✅ **Security Headers:** Implementación completa de OWASP best practices
- ✅ **Modularización:** Código organizado por responsabilidades
- ✅ **Dead Code Removal:** Eliminación de funcionalidades obsoletas
- ✅ **UI/UX Improvements:** Banner moderno con efectos sutiles
- ✅ **Sticky Footer:** Footer siempre visible en la parte inferior
- ✅ **JavaScript Organizado:** Código frontend estructurado con TOC

### SSL Multiplataforma (2025)

- 🔐 **truststore:** Certificados del sistema operativo (Windows/macOS/Linux)
- 🔄 **Fallback automático:** certifi si truststore no disponible
- 🪟 **Fix Windows:** Resuelve problemas SSL en Windows automáticamente
- 🍎 **macOS Keychain:** Integración nativa con certificados del sistema
- 🐧 **Linux:** Usa /etc/ssl/certs automáticamente

### Base de Datos Optimizada

- 📊 **Índices SQLite:** Búsquedas optimizadas en CUIT, nombre y apellido
- 🔍 **Fuzzy Matching:** Algoritmo mejorado para coincidencias parciales
- ⚡ **Performance:** Búsquedas rápidas incluso con 6M+ registros

---
**⚠️ DISCLAIMER:** Esta herramienta es solo para fines educativos. El uso indebido de esta herramienta puede ser ilegal. Usa bajo tu propia responsabilidad.
