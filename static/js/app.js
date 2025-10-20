/*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DEUDAS OSINT - Aplicación de Consulta BCRA y AFIP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  📋 TABLA DE CONTENIDOS
  
  1. CONFIG ........................... Configuración global
  2. UTILS ............................ Utilidades reutilizables
  3. UI ............................... Interfaz de usuario
  4. API .............................. Comunicación con backend
  5. APP .............................. Lógica principal
  6. FUNCIONES GLOBALES ............... Event handlers (window.*)
  7. INICIALIZACIÓN ................... Setup inicial

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
*/

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 1. CONFIGURACIÓN GLOBAL
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// Configuración global
const CONFIG = {
    API_BASE: '/',
    BANCOS_INFO: {} // Se carga dinámicamente desde /api/bancos_info
};

// Estado global de la aplicación
let currentData = null;
let modoDemo = false;

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 2. UTILIDADES (utils)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Funciones auxiliares reutilizables en toda la aplicación

// Utilidades
const utils = {
    // Formatear número como moneda argentina (en miles de pesos)
    formatCurrency: (amount) => {
        // Los montos vienen en miles de pesos, así que:
        // 1000K = 1,000,000 pesos = 1M
        // 100K = 100,000 pesos = 0.1M
        
        if (amount >= 1000) {  // 1,000K o más (1,000,000 pesos o más)
            return `$${(amount / 1000).toFixed(2)}M`;
        } else {  // Menos de 1,000K (menos de 1,000,000 pesos)
            return `$${amount.toLocaleString('es-AR')}K`;
        }
    },

    // Formatear monto detallado con separadores
    formatCurrencyDetailed: (amount) => {
        return `$${amount.toLocaleString('es-AR')}K`;
    },

    // Formatear CUIT
    formatCUIT: (cuit) => {
        // Convertir a string si viene como número
        const cuitStr = String(cuit);
        const clean = cuitStr.replace(/[-\s]/g, '');
        if (clean.length === 11) {
            return `${clean.slice(0, 2)}-${clean.slice(2, 10)}-${clean.slice(10)}`;
        }
        return cuitStr;
    },

    // Validar CUIT
    validateCUIT: (cuit) => {
        // Convertir a string si viene como número
        const cuitStr = String(cuit);
        const clean = cuitStr.replace(/[-\s]/g, '');
        const prefijos = ['20', '23', '24', '27', '30', '33', '34'];
        return clean.length === 11 && 
               clean.match(/^\d{11}$/) && 
               prefijos.includes(clean.slice(0, 2));
    },

    // Mostrar notificación
    showNotification: (message, type = 'info') => {
        // Crear elemento de notificación
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        // Agregar estilos
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 0.75rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            z-index: 1001;
            animation: slideIn 0.3s ease-out;
        `;
        
        document.body.appendChild(notification);
        
        // Remover después de 5 segundos
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    },

    // Debounce para input
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 3. INTERFAZ DE USUARIO (ui)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Funciones para manipular el DOM y renderizar la interfaz

// Funciones de UI
const ui = {
    // Mostrar sección
    showSection: (sectionId) => {
        const sections = ['consultaSection', 'loadingSection', 'resultsSection', 'errorSection'];
        sections.forEach(id => {
            const section = document.getElementById(id);
            if (section) {
                section.style.display = id === sectionId ? 'block' : 'none';
            }
        });
    },

    // Mostrar loading
    showLoading: () => {
        ui.showSection('loadingSection');
    },

    // Mostrar resultados
    showResults: (data) => {
        console.log('showResults llamado con datos:', data);
        currentData = data;
        ui.showSection('resultsSection');
        console.log('Llamando renderResumenGeneral...');
        ui.renderResumenGeneral(data);
        console.log('Llamando renderDeudasPorBanco...');
        ui.renderDeudasPorBanco(data);
    },

    // Mostrar error
    showError: (message) => {
        const errorSection = document.getElementById('errorSection');
        const errorMessage = document.getElementById('errorMessage');
        if (errorMessage) {
            errorMessage.textContent = message;
        }
        ui.showSection('errorSection');
    },

    // Renderizar resumen general
    renderResumenGeneral: (data) => {
        const container = document.getElementById('resumenGeneral');
        if (!container) {
            console.error('❌ No se encontró el contenedor resumenGeneral');
            return;
        }

        const { total_deuda, cantidad_total, bancos_afectados, denominacion, cuit_consultado } = data;
        
        // Debug: mostrar datos en consola
        console.log('Datos recibidos en renderResumenGeneral:', data);
        console.log('Denominacion:', denominacion);
        console.log('CUIT consultado:', cuit_consultado);
        
        // Mostrar nombre del usuario si está disponible
        const nombreUsuario = denominacion || 'Usuario';
        const cuitFormateado = cuit_consultado ? utils.formatCUIT(cuit_consultado) : '';
        
        console.log('Nombre usuario:', nombreUsuario);
        console.log('CUIT formateado:', cuitFormateado);
        
        container.innerHTML = `
            <div class="usuario-info mb-4" style="background: linear-gradient(135deg, #007bff, #0056b3); color: white; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <div class="usuario-nombre" style="display: flex; align-items: center; justify-content: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                    <i class="fas fa-user" style="font-size: 1.25rem; opacity: 0.9;"></i>
                    <span class="nombre" style="font-size: 1.5rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">${nombreUsuario}</span>
                </div>
                ${cuitFormateado ? `<div class="usuario-cuit" style="font-size: 0.875rem; opacity: 0.9; font-weight: 500;">CUIT: ${cuitFormateado}</div>` : ''}
            </div>
            <div class="resumen-stats">
                <div class="stat-card">
                    <div class="stat-value">${utils.formatCurrency(total_deuda)}</div>
                    <div class="stat-label">Total Adeudado</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${cantidad_total}</div>
                    <div class="stat-label">Productos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${bancos_afectados}</div>
                    <div class="stat-label">Bancos Afectados</div>
                </div>
            </div>
            <div class="text-center">
                <p class="mb-0">
                    <i class="fas fa-info-circle"></i>
                    Se encontraron deudas en ${bancos_afectados} ${bancos_afectados === 1 ? 'banco' : 'bancos'} 
                    por un total de ${utils.formatCurrency(total_deuda)} (${utils.formatCurrencyDetailed(total_deuda)})
                </p>
                <p class="text-muted small mt-2">
                    <i class="fas fa-exclamation-triangle"></i>
                    Los montos están expresados en miles de pesos argentinos
                </p>
            </div>
        `;
    },

    // Renderizar deudas por banco
    renderDeudasPorBanco: (data) => {
        const container = document.getElementById('deudasPorBanco');
        if (!container) return;

        const { deudas_por_banco } = data;
        
        if (Object.keys(deudas_por_banco).length === 0) {
            container.innerHTML = `
                <div class="text-center">
                    <i class="fas fa-check-circle" style="font-size: 3rem; color: #10b981; margin-bottom: 1rem;"></i>
                    <h3>¡Excelente noticia!</h3>
                    <p>No se encontraron deudas registradas en la Central de Deudores del BCRA para este CUIT.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = Object.entries(deudas_por_banco)
            .sort(([,a], [,b]) => b.total - a.total)
            .map(([banco, info]) => ui.renderBancoCard(banco, info))
            .join('');
    },

    // Renderizar tarjeta de banco
    renderBancoCard: (banco, info) => {
        // Nota: Ya no se usan email/telefono oficiales, solo datos fake en phishing

        // Obtener información de la situación principal
        const situacionInfo = info.situacion_principal || {};
        const situacionBadge = ui.renderSituacionBadge(situacionInfo);

        return `
            <div class="banco-card fade-in">
                <div class="banco-header">
                    <div class="banco-nombre">
                        <i class="fas fa-university"></i>
                        ${banco}
                    </div>
                    <div class="banco-monto">
                        <div class="monto-principal">${utils.formatCurrency(info.total)}</div>
                        <div class="monto-detallado">${utils.formatCurrencyDetailed(info.total)}</div>
                    </div>
                </div>
                
                ${situacionBadge}
                
                <div class="banco-details">
                    <div class="detail-item">
                        <div class="detail-value">${info.cantidad}</div>
                        <div class="detail-label">Productos</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-value">${info.dias_atraso_max}</div>
                        <div class="detail-label">Días Atraso</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-value">${info.situaciones.length}</div>
                        <div class="detail-label">Situaciones</div>
                    </div>
                </div>
                
                <div class="banco-actions">
                    <button class="btn btn-primary" onclick="generarCorreo('${banco}', ${JSON.stringify(info).replace(/"/g, '&quot;')})">
                        <i class="fas fa-eye"></i>
                        Visualizar Phishing
                    </button>
                    <button class="btn btn-secondary" onclick="verDetalles('${banco}', ${JSON.stringify(info).replace(/"/g, '&quot;')})">
                        <i class="fas fa-info-circle"></i>
                        Ver Detalles
                    </button>
                </div>
            </div>
        `;
    },

    // Renderizar badge de situación crediticia
    renderSituacionBadge: (situacionInfo) => {
        if (!situacionInfo || !situacionInfo.descripcion) {
            return '';
        }

        const { descripcion, riesgo, color, icono, explicacion } = situacionInfo;
        
        return `
            <div class="situacion-info">
                <div class="situacion-badge ${color}">
                    <i class="fas fa-${icono}"></i>
                    <span>${descripcion}</span>
                </div>
                <div class="situacion-explicacion">
                    <strong>${riesgo}:</strong> ${explicacion}
                </div>
            </div>
        `;
    }
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 4. COMUNICACIÓN API (api)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Funciones para comunicación con el backend Flask

// Funciones de API
const api = {
    // Consultar deudas
    consultarDeudas: async (cuit) => {
        try {
            const response = await fetch('/consultar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ cuit })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Error en la consulta');
            }

            return data;
        } catch (error) {
            throw new Error(error.message || 'Error de conexión');
        }
    }
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 5. APLICACIÓN PRINCIPAL (app)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Lógica principal de la aplicación y manejo de eventos

// Funciones principales
const app = {
    // Inicializar aplicación
    init: async () => {
        console.log('🚀 Inicializando aplicación de consulta de deudas BCRA');
        
        // Nota: Ya no cargamos datos oficiales de bancos (email/telefono)
        // Solo se usan datos fake para phishing educativo
        
        // Configurar formulario
        const form = document.getElementById('consultaForm');
        const cuitInput = document.getElementById('cuit');
        const consultarBtn = document.getElementById('consultarBtn');

        if (form) {
            form.addEventListener('submit', app.handleSubmit);
        }

        if (cuitInput) {
            // Formatear CUIT mientras se escribe
            cuitInput.addEventListener('input', utils.debounce((e) => {
                const value = e.target.value.replace(/[^\d]/g, '');
                if (value.length <= 11) {
                    let formatted = value;
                    if (value.length > 2) {
                        formatted = value.slice(0, 2) + '-' + value.slice(2);
                    }
                    if (value.length > 10) {
                        formatted = value.slice(0, 2) + '-' + value.slice(2, 10) + '-' + value.slice(10);
                    }
                    e.target.value = formatted;
                }
            }, 300));

            // Validar en tiempo real
            cuitInput.addEventListener('input', utils.debounce((e) => {
                const isValid = utils.validateCUIT(e.target.value);
                cuitInput.style.borderColor = isValid ? '#10b981' : '#ef4444';
            }, 500));
        }

        // Mostrar sección inicial
        ui.showSection('consultaSection');
    },

    // Manejar envío del formulario
    handleSubmit: async (e) => {
        e.preventDefault();
        
        const cuitInput = document.getElementById('cuit');
        const consultarBtn = document.getElementById('consultarBtn');
        const cuit = cuitInput.value.trim();

        // Validar CUIT
        if (!cuit) {
            utils.showNotification('Debe ingresar un CUIT', 'error');
            return;
        }

        if (!utils.validateCUIT(cuit)) {
            utils.showNotification('Formato de CUIT inválido', 'error');
            return;
        }

        // Mostrar loading
        ui.showLoading();
        consultarBtn.disabled = true;

        try {
            // Consultar API
            const data = await api.consultarDeudas(cuit);
            
            // Mostrar resultados
            ui.showResults(data);
            utils.showNotification('Consulta realizada exitosamente', 'success');
            
        } catch (error) {
            console.error('Error en consulta:', error);
            ui.showError(error.message);
            utils.showNotification(error.message, 'error');
        } finally {
            consultarBtn.disabled = false;
        }
    }
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 6. FUNCIONES GLOBALES (window.*)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Funciones expuestas globalmente para event handlers HTML (onclick, etc)
// IMPORTANTE: NO eliminar estas funciones - el HTML las referencia directamente

// ─────────────────────────────────────────────────────────────────────────
// 6.1. NAVEGACIÓN
// ─────────────────────────────────────────────────────────────────────────

// Funciones globales para botones
window.nuevaConsulta = () => {
    ui.showSection('consultaSection');
    document.getElementById('cuit').value = '';
    currentData = null;
};

// ─────────────────────────────────────────────────────────────────────────
// 6.2. MODALES Y DISCLAIMERS
// ─────────────────────────────────────────────────────────────────────────

// Función para toggle del disclaimer flotante
window.toggleDisclaimer = () => {
    const disclaimerContent = document.getElementById('disclaimerContent');
    const disclaimerToggle = document.querySelector('.disclaimer-toggle');
    
    if (disclaimerContent.classList.contains('show')) {
        disclaimerContent.classList.remove('show');
        disclaimerToggle.style.transform = 'scale(1)';
    } else {
        disclaimerContent.classList.add('show');
        disclaimerToggle.style.transform = 'scale(1.1)';
    }
};

// Funciones para modales modernos
window.abrirModalDisclaimer = () => {
    const modal = document.getElementById('disclaimerModal');
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
};

window.cerrarModalDisclaimer = () => {
    const modal = document.getElementById('disclaimerModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
};

window.abrirModalTecnico = () => {
    const modal = document.getElementById('tecnicoModal');
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
};

window.cerrarModalTecnico = () => {
    const modal = document.getElementById('tecnicoModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
};

// Cerrar modales al hacer click fuera
window.onclick = (event) => {
    const disclaimerModal = document.getElementById('disclaimerModal');
    const tecnicoModal = document.getElementById('tecnicoModal');
    const detallesModal = document.getElementById('detallesModal');
    
    if (event.target === disclaimerModal) {
        cerrarModalDisclaimer();
    }
    if (event.target === tecnicoModal) {
        cerrarModalTecnico();
    }
    if (event.target === detallesModal) {
        cerrarModalDetalles();
    }
};

// ─────────────────────────────────────────────────────────────────────────
// 6.3. PHISHING EDUCATIVO
// ─────────────────────────────────────────────────────────────────────────

window.generarCorreo = async (banco, deudaInfo) => {
    if (!currentData) return;

    try {
        // Obtener datos del usuario
        const nombreUsuario = currentData.nombre || 'Usuario';
        const montoDeuda = deudaInfo.total || '$0';
        
        // Generar fecha vencida (un día antes de hoy)
        const hoy = new Date();
        const ayer = new Date(hoy);
        ayer.setDate(hoy.getDate() - 1);
        const fechaVencimiento = ayer.toLocaleDateString('es-AR', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
        });

        // Generar template de phishing educativo
        const response = await fetch('/visualizar_correo_phishing', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                banco: banco,
                nombre_usuario: nombreUsuario,
                monto_deuda: montoDeuda,
                fecha_vencimiento: fechaVencimiento
            })
        });

        if (response.ok) {
            // Obtener el HTML del correo
            const htmlContent = await response.text();
            
            // Abrir en nueva pestaña
            const nuevaVentana = window.open('', '_blank', 'width=800,height=600,scrollbars=yes,resizable=yes');
            nuevaVentana.document.write(htmlContent);
            nuevaVentana.document.close();
            
            // Enfocar la nueva ventana
            nuevaVentana.focus();
            
            utils.showNotification('Correo phishing educativo abierto en nueva pestaña', 'success');
        } else {
            const errorData = await response.json();
            utils.showNotification('Error generando correo: ' + errorData.error, 'error');
        }
        
    } catch (error) {
        utils.showNotification('Error generando correo phishing', 'error');
        console.error('Error:', error);
    }
};


// ─────────────────────────────────────────────────────────────────────────
// 6.4. VISUALIZACIÓN DE DETALLES DE DEUDAS
// ─────────────────────────────────────────────────────────────────────────

window.verDetalles = (banco, deudaInfo) => {
    try {
        console.log('verDetalles llamado para banco:', banco);
        console.log('currentData:', currentData);
        
        // Obtener todas las deudas de este banco desde currentData
        let deudasDelBanco = [];
        if (currentData && currentData.deudas) {
            console.log('Todas las deudas disponibles:', currentData.deudas);
            console.log('Buscando banco:', banco);
            
            deudasDelBanco = currentData.deudas.filter(deuda => {
                console.log('Comparando:', deuda.entidadFinanciera, 'con', banco);
                return deuda.entidadFinanciera === banco;
            });
            console.log('deudasDelBanco encontradas:', deudasDelBanco);
            
            // Si no se encuentran coincidencias exactas, intentar búsqueda parcial
            if (deudasDelBanco.length === 0) {
                console.log('No se encontraron coincidencias exactas, intentando búsqueda parcial...');
                deudasDelBanco = currentData.deudas.filter(deuda => 
                    deuda.entidadFinanciera && deuda.entidadFinanciera.includes(banco) ||
                    banco.includes(deuda.entidadFinanciera)
                );
                console.log('deudasDelBanco con búsqueda parcial:', deudasDelBanco);
            }
        } else {
            console.log('No hay currentData o deudas disponibles');
        }
        
        // Crear contenido detallado
        let detallesContent = `
            <div class="detalles-header">
                <h3><i class="fas fa-university"></i> ${banco}</h3>
                <div class="detalles-resumen">
                    <div class="resumen-item">
                        <span class="resumen-label">Total Deuda</span>
                        <span class="resumen-value">${utils.formatCurrency(deudaInfo.total)}</span>
                    </div>
                    <div class="resumen-item">
                        <span class="resumen-label">Productos</span>
                        <span class="resumen-value">${deudaInfo.cantidad}</span>
                    </div>
                    <div class="resumen-item">
                        <span class="resumen-label">Días Atraso</span>
                        <span class="resumen-value">${deudaInfo.dias_atraso_max}</span>
                    </div>
                </div>
            </div>
            <div class="detalles-content">
        `;
        
        // Mostrar cada deuda individual con todos los datos de la API
        if (deudasDelBanco.length > 0) {
            deudasDelBanco.forEach((deuda, index) => {
                console.log('Procesando deuda individual:', deuda);
                
                const situacionInfo = deuda.situacionInfo || {};
                const fechaSit1 = deuda.fechaVencimiento || deuda.fechaSit1 || 'No especificada';
                const monto = deuda.montoDetallado || utils.formatCurrencyDetailed(deuda.montoDeuda);
                
                // Mostrar todos los campos disponibles para debug
                console.log('Campos de la deuda:', Object.keys(deuda));
                console.log('procesoJud:', deuda.procesoJud);
                console.log('refinanciaciones:', deuda.refinanciaciones);
                console.log('situacionJuridica:', deuda.situacionJuridica);
                
                detallesContent += `
                    <div class="deuda-item">
                        <div class="deuda-header">
                            <h4>Producto ${index + 1}</h4>
                            <div class="deuda-monto">${monto}</div>
                        </div>
                        <div class="deuda-details">
                            <div class="detail-row">
                                <span class="detail-label">Situación:</span>
                                <span class="detail-value situacion-${situacionInfo.color || 'secondary'}">
                                    <i class="fas fa-${situacionInfo.icono || 'question-circle'}"></i>
                                    ${situacionInfo.descripcion || deuda.situacion || 'No especificada'}
                                </span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Fecha Situación:</span>
                                <span class="detail-value">${fechaSit1}</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Días Atraso:</span>
                                <span class="detail-value">${deuda.diasAtraso || deuda.diasAtrasoPago || 0}</span>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Moneda:</span>
                                <span class="detail-value">${deuda.moneda || 'ARS'}</span>
                            </div>
                        </div>
                        <div class="deuda-flags">
                            <div class="flag-item ${deuda.refinanciaciones ? 'flag-active' : 'flag-inactive'}">
                                <i class="fas fa-${deuda.refinanciaciones ? 'check' : 'times'}"></i>
                                <span>Refinanciaciones: ${deuda.refinanciaciones ? 'Sí' : 'No'}</span>
                            </div>
                            <div class="flag-item ${deuda.recategorizacionOblig ? 'flag-active' : 'flag-inactive'}">
                                <i class="fas fa-${deuda.recategorizacionOblig ? 'check' : 'times'}"></i>
                                <span>Recategorización Obligatoria: ${deuda.recategorizacionOblig ? 'Sí' : 'No'}</span>
                            </div>
                            <div class="flag-item ${deuda.situacionJuridica ? 'flag-active' : 'flag-inactive'}">
                                <i class="fas fa-${deuda.situacionJuridica ? 'check' : 'times'}"></i>
                                <span>Situación Jurídica: ${deuda.situacionJuridica ? 'Sí' : 'No'}</span>
                            </div>
                            <div class="flag-item ${deuda.irrecDisposicionTecnica ? 'flag-active' : 'flag-inactive'}">
                                <i class="fas fa-${deuda.irrecDisposicionTecnica ? 'check' : 'times'}"></i>
                                <span>Irrec. Disposición Técnica: ${deuda.irrecDisposicionTecnica ? 'Sí' : 'No'}</span>
                            </div>
                            <div class="flag-item ${deuda.enRevision ? 'flag-active' : 'flag-inactive'}">
                                <i class="fas fa-${deuda.enRevision ? 'check' : 'times'}"></i>
                                <span>En Revisión: ${deuda.enRevision ? 'Sí' : 'No'}</span>
                            </div>
                            <div class="flag-item ${deuda.procesoJud ? 'flag-active' : 'flag-inactive'}">
                                <i class="fas fa-${deuda.procesoJud ? 'check' : 'times'}"></i>
                                <span>Proceso Judicial: ${deuda.procesoJud ? 'Sí' : 'No'}</span>
                            </div>
                        </div>
                    </div>
                `;
            });
        } else {
            // Si no hay datos individuales, crear un producto simulado con los datos disponibles
            console.log('No se encontraron deudas individuales, creando producto simulado...');
            console.log('deudaInfo disponible:', deudaInfo);
            
            const situacionInfo = deudaInfo.situacion_principal || {};
            const monto = deudaInfo.total || 0;
            
            detallesContent += `
                <div class="deuda-item">
                    <div class="deuda-header">
                        <h4>Producto 1</h4>
                        <div class="deuda-monto">${utils.formatCurrency(monto)}</div>
                    </div>
                    <div class="deuda-details">
                        <div class="detail-row">
                            <span class="detail-label">Situación:</span>
                            <span class="detail-value situacion-${situacionInfo.color || 'secondary'}">
                                <i class="fas fa-${situacionInfo.icono || 'question-circle'}"></i>
                                ${situacionInfo.descripcion || 'No especificada'}
                            </span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Días Atraso:</span>
                            <span class="detail-value">${deudaInfo.dias_atraso_max || 0}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Moneda:</span>
                            <span class="detail-value">ARS</span>
                        </div>
                    </div>
                    <div class="deuda-flags">
                        <div class="flag-item flag-inactive">
                            <i class="fas fa-times"></i>
                            <span>Refinanciaciones: No</span>
                        </div>
                        <div class="flag-item flag-inactive">
                            <i class="fas fa-times"></i>
                            <span>Recategorización Obligatoria: No</span>
                        </div>
                        <div class="flag-item flag-inactive">
                            <i class="fas fa-times"></i>
                            <span>Situación Jurídica: No</span>
                        </div>
                        <div class="flag-item flag-inactive">
                            <i class="fas fa-times"></i>
                            <span>Irrec. Disposición Técnica: No</span>
                        </div>
                        <div class="flag-item flag-inactive">
                            <i class="fas fa-times"></i>
                            <span>En Revisión: No</span>
                        </div>
                        <div class="flag-item flag-inactive">
                            <i class="fas fa-times"></i>
                            <span>Proceso Judicial: No</span>
                        </div>
                    </div>
                    <div class="deuda-flags">
                        <div class="flag-item flag-info">
                            <i class="fas fa-info-circle"></i>
                            <span>Información consolidada - Datos individuales no disponibles</span>
                        </div>
                    </div>
                </div>
            `;
        }
        
        detallesContent += `</div>`;
        
        // Mostrar modal
        mostrarModalDetalles(detallesContent);
    } catch (error) {
        console.error('Error en verDetalles:', error);
        alert('Error al mostrar detalles: ' + error.message);
    }
};

// Función para mostrar modal de detalles
window.mostrarModalDetalles = (content) => {
    try {
        const modal = document.getElementById('detallesModal');
        const modalBody = document.getElementById('detallesModalBody');
        
        if (!modal || !modalBody) {
            alert('Error: Modal no encontrado');
            return;
        }
        
        modalBody.innerHTML = content;
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    } catch (error) {
        console.error('Error en mostrarModalDetalles:', error);
        alert('Error al mostrar modal: ' + error.message);
    }
};

// Función para cerrar modal de detalles
window.cerrarModalDetalles = () => {
    const modal = document.getElementById('detallesModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
};

// Función de prueba para el modal
window.testModal = () => {
    try {
        const testContent = `
            <div class="detalles-header">
                <h3><i class="fas fa-university"></i> Banco de Prueba</h3>
                <div class="detalles-resumen">
                    <div class="resumen-item">
                        <span class="resumen-label">Total Deuda</span>
                        <span class="resumen-value">$100K</span>
                    </div>
                    <div class="resumen-item">
                        <span class="resumen-label">Productos</span>
                        <span class="resumen-value">2</span>
                    </div>
                    <div class="resumen-item">
                        <span class="resumen-label">Días Atraso</span>
                        <span class="resumen-value">30</span>
                    </div>
                </div>
            </div>
            <div class="detalles-content">
                <div class="deuda-item">
                    <div class="deuda-header">
                        <h4>Información del Banco</h4>
                        <div class="deuda-monto">$100K</div>
                    </div>
                    <div class="deuda-details">
                        <div class="detail-row">
                            <span class="detail-label">Situación Principal:</span>
                            <span class="detail-value situacion-info">
                                <i class="fas fa-info-circle"></i>
                                Con seguimiento especial
                            </span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Días de Atraso Máximo:</span>
                            <span class="detail-value">30</span>
                        </div>
                    </div>
                    <div class="deuda-flags">
                        <div class="flag-item flag-info">
                            <i class="fas fa-info-circle"></i>
                            <span>Información de prueba</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        mostrarModalDetalles(testContent);
    } catch (error) {
        console.error('Error en testModal:', error);
        alert('Error en prueba: ' + error.message);
    }
};




// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 7. INICIALIZACIÓN DE LA APLICACIÓN
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', app.init);

// Event listener para el botón de demo
document.addEventListener('DOMContentLoaded', function() {
    const demoBtn = document.getElementById('demoBtn');
    if (demoBtn) {
        demoBtn.addEventListener('click', function() {
            cargarModoDemo();
        });
    }
});

// Agregar estilos para animaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification {
        animation: slideIn 0.3s ease-out;
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
`;
document.head.appendChild(style);

// Funciones para el modo demo
window.cargarModoDemo = async function() {
    try {
        console.log('🎭 Cargando modo demo...');
        
        // Obtener datos de demo del servidor
        const response = await fetch('/demo_cuit');
        const demoData = await response.json();
        
        // Llenar el campo CUIT con el CUIT de demo
        const cuitInput = document.getElementById('cuit');
        if (cuitInput) {
            cuitInput.value = demoData.cuit_demo;
        }
        
        // Activar modo demo
        modoDemo = true;
        
        // Mostrar notificación
        mostrarNotificacion('Modo Demo activado - Usando datos ficticios para demostración', 'info');
        
        // Ejecutar consulta automáticamente
        setTimeout(() => {
            ejecutarConsulta();
        }, 1000);
        
    } catch (error) {
        console.error('Error cargando modo demo:', error);
        mostrarNotificacion('Error cargando modo demo', 'error');
    }
};

// Función para mostrar notificaciones
function mostrarNotificacion(mensaje, tipo = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${tipo}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${tipo === 'info' ? 'info-circle' : tipo === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            <span>${mensaje}</span>
        </div>
    `;
    
    // Agregar estilos si no existen
    if (!document.getElementById('notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--bg-card);
                border: var(--border);
                border-radius: var(--border-radius);
                padding: 1rem 1.5rem;
                box-shadow: var(--shadow-lg);
                z-index: 1000;
                animation: slideIn 0.3s ease-out;
                max-width: 400px;
            }
            
            .notification-info {
                border-left: 4px solid var(--accent-blue);
            }
            
            .notification-success {
                border-left: 4px solid #10b981;
            }
            
            .notification-error {
                border-left: 4px solid #ef4444;
            }
            
            .notification-content {
                display: flex;
                align-items: center;
                gap: 0.75rem;
                color: var(--text-primary);
            }
            
            .notification-content i {
                font-size: 1.2rem;
            }
            
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Agregar al DOM
    document.body.appendChild(notification);
    
    // Remover después de 5 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// ─────────────────────────────────────────────────────────────────────────
// 6.5. BÚSQUEDA AFIP Y MODO DEMO
// ─────────────────────────────────────────────────────────────────────────

// Cambiar entre tabs
window.cambiarTab = function(tab) {
    // Actualizar botones
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.closest('.tab-button').classList.add('active');
    
    // Actualizar contenido
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
        content.style.display = 'none';
    });
    
    if (tab === 'cuit') {
        document.getElementById('tabCuit').classList.add('active');
        document.getElementById('tabCuit').style.display = 'block';
    } else if (tab === 'nombre') {
        document.getElementById('tabNombre').classList.add('active');
        document.getElementById('tabNombre').style.display = 'block';
    }
};

// Manejar formulario de búsqueda por nombre
document.getElementById('busquedaNombreForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const apellido = document.getElementById('apellido').value.trim();
    const nombre = document.getElementById('nombre').value.trim();
    const btn = document.getElementById('buscarNombreBtn');
    const spinner = btn.querySelector('.spinner');
    const span = btn.querySelector('span');
    
    if (!apellido) {
        utils.showNotification('Debe ingresar al menos un apellido', 'error');
        return;
    }
    
    // Mostrar loading
    btn.disabled = true;
    spinner.style.display = 'inline-block';
    span.textContent = 'Buscando...';
    
    try {
        const response = await fetch('/buscar_por_nombre', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                apellido: apellido,
                nombre: nombre
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            mostrarResultadosBusqueda(data.resultados, data.query);
            utils.showNotification(`Se encontraron ${data.total} resultados`, 'success');
        } else {
            utils.showNotification(data.error || 'Error en la búsqueda', 'error');
            
            // Si la base de datos no está disponible, mostrar instrucciones
            if (data.instrucciones) {
                utils.showNotification('Ejecute el script de importación primero', 'info');
            }
        }
    } catch (error) {
        console.error('Error en búsqueda:', error);
        utils.showNotification('Error al buscar contribuyentes', 'error');
    } finally {
        // Restaurar botón
        btn.disabled = false;
        spinner.style.display = 'none';
        span.textContent = 'Buscar Contribuyentes';
    }
});

// Mostrar resultados de búsqueda
function mostrarResultadosBusqueda(resultados, query) {
    const container = document.getElementById('resultadosBusquedaNombre');
    const lista = document.getElementById('listaResultados');
    const totalBadge = document.getElementById('totalResultados');
    
    // Limpiar resultados anteriores
    lista.innerHTML = '';
    
    // Agregar disclaimer SIEMPRE antes de los resultados
    const disclaimer = document.createElement('div');
    disclaimer.className = 'busqueda-disclaimer-info';
    disclaimer.innerHTML = `
        <div class="disclaimer-header-info">
            <i class="fas fa-info-circle"></i>
            <strong>Importante</strong>
        </div>
        <div class="disclaimer-body-info">
            Esta búsqueda solo incluye personas inscriptas como <strong>monotributistas o responsables inscriptos en AFIP</strong>. 
            La persona que buscas puede no estar en esta base de datos si no cumple con estos requisitos.
        </div>
    `;
    lista.appendChild(disclaimer);
    
    if (resultados.length === 0) {
        lista.innerHTML = `
            <div class="resultado-item" style="justify-content: center; cursor: default;">
                <div style="text-align: center; padding: 2rem;">
                    <i class="fas fa-search" style="font-size: 3rem; color: var(--text-muted); margin-bottom: 1rem;"></i>
                    <p style="color: var(--text-muted);">No se encontraron resultados para "${query.apellido}${query.nombre ? ' ' + query.nombre : ''}"</p>
                </div>
            </div>
        `;
        container.style.display = 'block';
        totalBadge.textContent = '0 resultados';
        return;
    }
    
    // Actualizar badge de total
    totalBadge.textContent = `${resultados.length} resultado${resultados.length !== 1 ? 's' : ''}`;
    
    // Renderizar resultados
    resultados.forEach(resultado => {
        const item = document.createElement('div');
        item.className = 'resultado-item';
        
        // Función helper para obtener descripción de códigos AFIP
        const getDescripcionAFIP = (tipo, codigo) => {
            const descripciones = {
                monotributo: {
                    'BT': 'B trabajador promovido',
                    'AP': 'A actividad primaria',
                    'AC': 'A asociado a cooperativa',
                    'AL': 'A monotributo social locación',
                    'AV': 'A monotributo social ventas',
                    'AT': 'A trabajador promovido',
                    'NI': 'No Inscripto'
                },
                iva: {
                    'NI': 'No Inscripto',
                    'AC': 'Activo',
                    'EX': 'Exento',
                    'NA': 'No alcanzado',
                    'XN': 'Exento no alcanzado',
                    'AN': 'Activo no alcanzado',
                    'NC': 'No corresponde'
                },
                ganancias: {
                    'NI': 'No Inscripto',
                    'AC': 'Activo',
                    'EX': 'Exento',
                    'NC': 'No corresponde'
                },
                actividad: {
                    '0': 'No es monotributista',
                    '00': 'No es monotributista',
                    '01': 'Comercial',
                    '1': 'Comercial',
                    '02': 'Profesional',
                    '2': 'Profesional',
                    '03': 'Servicios/Oficio',
                    '3': 'Servicios/Oficio',
                    '04': 'Industrial',
                    '4': 'Industrial',
                    '05': 'Agropecuaria',
                    '5': 'Agropecuaria',
                    '06': 'Otros',
                    '6': 'Otros',
                    '07': 'Eventual',
                    '7': 'Eventual',
                    '08': 'Prest. de Servicio o Locación',
                    '8': 'Prest. de Servicio o Locación',
                    '09': 'Otras actividades',
                    '9': 'Otras actividades',
                    '10': 'Ventas',
                    '11': 'Agricultura Familia'
                }
            };
            return descripciones[tipo]?.[codigo] || codigo;
        };
        
        // Badges de impuestos con tooltips personalizados
        let badges = '';
        
        // Monotributo
        if (resultado.monotributo && resultado.monotributo !== 'NI') {
            const desc = getDescripcionAFIP('monotributo', resultado.monotributo);
            badges += `
                <span class="resultado-badge monotributo" data-tooltip="Monotributo: ${desc}">
                    Monotributo ${resultado.monotributo}
                    <span class="badge-tooltip">Monotributo: ${desc}</span>
                </span>`;
        }
        
        // IVA (mostrar siempre, incluso NI)
        if (resultado.imp_iva) {
            const desc = getDescripcionAFIP('iva', resultado.imp_iva);
            const badgeClass = resultado.imp_iva === 'NI' ? 'neutral' : 'iva';
            badges += `
                <span class="resultado-badge ${badgeClass}" data-tooltip="Impuesto IVA: ${desc}">
                    Imp IVA: ${resultado.imp_iva}
                    <span class="badge-tooltip">Impuesto IVA: ${desc}</span>
                </span>`;
        }
        
        // Ganancias (mostrar siempre, incluso NI)
        if (resultado.imp_ganancias) {
            const desc = getDescripcionAFIP('ganancias', resultado.imp_ganancias);
            const badgeClass = resultado.imp_ganancias === 'NI' ? 'neutral' : 'ganancias';
            badges += `
                <span class="resultado-badge ${badgeClass}" data-tooltip="Impuesto a Ganancias: ${desc}">
                    Imp Ganancias: ${resultado.imp_ganancias}
                    <span class="badge-tooltip">Impuesto a Ganancias: ${desc}</span>
                </span>`;
        }
        
        // Integrante Sociedad (mostrar siempre)
        if (resultado.integrante_soc) {
            const desc = resultado.integrante_soc === 'S' ? 'Es integrante de sociedad' : 'No es integrante de sociedad';
            const badgeClass = resultado.integrante_soc === 'S' ? 'info' : 'neutral';
            badges += `
                <span class="resultado-badge ${badgeClass}" data-tooltip="${desc}">
                    Integrante Soc.: ${resultado.integrante_soc}
                    <span class="badge-tooltip">${desc}</span>
                </span>`;
        }
        
        // Empleador (mostrar siempre)
        if (resultado.empleador) {
            const desc = resultado.empleador === 'S' ? 'Es empleador' : 'No es empleador';
            const badgeClass = resultado.empleador === 'S' ? 'info' : 'neutral';
            badges += `
                <span class="resultado-badge ${badgeClass}" data-tooltip="${desc}">
                    Empleador: ${resultado.empleador}
                    <span class="badge-tooltip">${desc}</span>
                </span>`;
        }
        
        // Actividad Monotributo (mostrar siempre)
        if (resultado.actividad_monotributo) {
            const desc = getDescripcionAFIP('actividad', resultado.actividad_monotributo);
            const badgeClass = (resultado.actividad_monotributo === '0' || resultado.actividad_monotributo === '00') ? 'neutral' : 'actividad';
            badges += `
                <span class="resultado-badge ${badgeClass}" data-tooltip="Actividad: ${desc}">
                    Actividad: ${resultado.actividad_monotributo}
                    <span class="badge-tooltip">Actividad: ${desc}</span>
                </span>`;
        }
        
        item.innerHTML = `
            <div class="resultado-info">
                <div class="resultado-nombre">
                    <i class="fas fa-user"></i>
                    ${resultado.denominacion}
                </div>
                <div class="resultado-cuit">
                    <i class="fas fa-id-card"></i>
                    ${utils.formatCUIT(resultado.cuit)}
                </div>
                ${badges ? `<div class="resultado-badges">${badges}</div>` : ''}
            </div>
            <div class="resultado-actions">
                <div class="match-score ${
                    resultado.match_score === 100 ? 'match-exact' : 
                    resultado.match_score >= 95 ? 'match-high' : 
                    resultado.match_score >= 80 ? 'match-moderate' : 
                    resultado.match_score >= 60 ? 'match-low' : 
                    'match-partial'
                }">
                    <i class="fas fa-${
                        resultado.match_score === 100 ? 'check-circle' : 
                        resultado.match_score >= 95 ? 'star' : 
                        resultado.match_score >= 80 ? 'bolt' : 
                        resultado.match_score >= 60 ? 'chart-bar' : 
                        'search'
                    }"></i>
                    ${
                        resultado.match_score === 100 ? 'Coincidencia exacta' : 
                        resultado.match_score >= 95 ? 'Alta similitud' : 
                        resultado.match_score >= 80 ? 'Similitud moderada' : 
                        resultado.match_score >= 60 ? 'Similitud baja' : 
                        'Coincidencia parcial'
                    }
                </div>
                <button class="btn-resultado" onclick="consultarDesdeBusqueda('${resultado.cuit}', '${resultado.denominacion}')">
                    <i class="fas fa-search"></i>
                    Consultar BCRA
                </button>
            </div>
        `;
        
        lista.appendChild(item);
    });
    
    // Mostrar container
    container.style.display = 'block';
    
    // Scroll suave hacia resultados
    setTimeout(() => {
        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

// Consultar BCRA desde resultado de búsqueda
window.consultarDesdeBusqueda = async function(cuit, nombre) {
    // Cambiar al tab de CUIT
    document.querySelectorAll('.tab-button')[0].click();
    
    // Llenar el input con el CUIT
    const cuitInput = document.getElementById('cuit');
    cuitInput.value = utils.formatCUIT(cuit);
    
    // Mostrar notificación
    utils.showNotification(`Consultando deudas de ${nombre}...`, 'info');
    
    // Trigger del formulario
    document.getElementById('consultaForm').dispatchEvent(new Event('submit'));
};
