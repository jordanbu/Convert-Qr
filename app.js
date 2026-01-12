// Estado de la aplicación
let qrCodeInstance = null;
let currentQrDataUrl = null;
let currentUrl = '';
let currentExpirationDate = null;

// Elementos del DOM
const qrForm = document.getElementById('qrForm');
const urlInput = document.getElementById('url');
const urlError = document.getElementById('urlError');
const expirationInput = document.getElementById('expiration');
const expirationHelp = document.getElementById('expirationHelp');
const sizeInput = document.getElementById('size');
const sizeHelp = document.getElementById('sizeHelp');
const metadataCheckbox = document.getElementById('metadata');
const metadataHelp = document.getElementById('metadataHelp');
const resetBtn = document.getElementById('resetBtn');
const qrPlaceholder = document.getElementById('qrPlaceholder');
const qrResult = document.getElementById('qrResult');
const qrcodeDiv = document.getElementById('qrcode');
const urlInfo = document.getElementById('urlInfo');
const urlText = document.getElementById('urlText');
const expirationInfo = document.getElementById('expirationInfo');
const expirationText = document.getElementById('expirationText');
const warningBox = document.getElementById('warningBox');
const infoBox = document.getElementById('infoBox');
const downloadBtn = document.getElementById('downloadBtn');

// Validar URL
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

// Actualizar texto de ayuda de expiración
expirationInput.addEventListener('input', function() {
    const months = parseInt(this.value) || 1;
    expirationHelp.textContent = `${months} ${months === 1 ? 'mes' : 'meses'} desde ahora`;
});

// Actualizar texto de ayuda de tamaño
sizeInput.addEventListener('input', function() {
    const size = parseInt(this.value);
    sizeHelp.textContent = `${size}x${size}px`;
});

// Validar URL en tiempo real
urlInput.addEventListener('input', function() {
    const url = this.value.trim();
    if (url && !isValidUrl(url)) {
        this.classList.add('invalid');
        urlError.style.display = 'block';
    } else {
        this.classList.remove('invalid');
        urlError.style.display = 'none';
    }
});

// Actualizar texto de ayuda de metadata
metadataCheckbox.addEventListener('change', function() {
    if (this.checked) {
        metadataHelp.textContent = 'El QR contendrá un JSON con la URL y fechas. Necesitarás una app que valide la fecha.';
    } else {
        metadataHelp.textContent = 'El QR contendrá solo la URL. No hay validación real de expiración.';
    }
});

// Generar QR
qrForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const url = urlInput.value.trim();
    
    if (!url) {
        alert('Por favor ingresa una URL válida');
        return;
    }

    if (!isValidUrl(url)) {
        alert('Por favor ingresa una URL válida (debe comenzar con http:// o https://)');
        return;
    }

    const expirationMonths = parseInt(expirationInput.value) || 12;
    const qrSize = parseInt(sizeInput.value) || 256;
    const includeMetadata = metadataCheckbox.checked;

    // Calcular fecha de expiración
    const expDate = new Date();
    expDate.setMonth(expDate.getMonth() + expirationMonths);
    currentExpirationDate = expDate;
    currentUrl = url;

    // Preparar contenido del QR
    let qrContent;
    if (includeMetadata) {
        const metadata = {
            url: url,
            creado: new Date().toISOString(),
            expira: expDate.toISOString(),
            nota: 'Este QR contiene metadata. Tu aplicación debe validar la fecha de expiración.'
        };
        qrContent = JSON.stringify(metadata);
    } else {
        qrContent = url;
    }

    try {
        // Limpiar QR anterior si existe
        qrcodeDiv.innerHTML = '';
        
        // Generar nuevo QR
        qrCodeInstance = new QRCode(qrcodeDiv, {
            text: qrContent,
            width: qrSize,
            height: qrSize,
            colorDark: "#000000",
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.L
        });

        // Esperar a que se genere el canvas
        setTimeout(() => {
            const canvas = qrcodeDiv.querySelector('canvas');
            const img = qrcodeDiv.querySelector('img');
            
            if (canvas) {
                currentQrDataUrl = canvas.toDataURL();
                
                // Asegurar que el QR sea visible
                canvas.style.display = 'block';
                canvas.style.margin = '0 auto';
                
                // Mostrar resultado
                qrPlaceholder.style.display = 'none';
                qrResult.style.display = 'flex';
                resetBtn.style.display = 'block';
                
                // Mostrar información
                if (!includeMetadata) {
                    urlText.textContent = url;
                    urlInfo.style.display = 'block';
                    warningBox.style.display = 'block';
                    infoBox.style.display = 'none';
                } else {
                    urlInfo.style.display = 'none';
                    warningBox.style.display = 'none';
                    infoBox.style.display = 'block';
                }
                
                // Mostrar fecha de expiración
                expirationText.textContent = expDate.toLocaleDateString('es-ES', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                });
                expirationInfo.style.display = 'block';
            } else {
                alert('Error al generar el código QR');
            }
        }, 100);
    } catch (err) {
        console.error('Error generando QR:', err);
        alert('Error al generar el código QR: ' + err.message);
    }
});

// Descargar QR
downloadBtn.addEventListener('click', function() {
    if (!currentQrDataUrl) return;
    
    const link = document.createElement('a');
    link.download = `qr-code-${Date.now()}.png`;
    link.href = currentQrDataUrl;
    link.click();
});

// Resetear formulario
resetBtn.addEventListener('click', function() {
    urlInput.value = '';
    urlInput.classList.remove('invalid');
    urlError.style.display = 'none';
    qrcodeDiv.innerHTML = '';
    currentQrDataUrl = null;
    currentUrl = '';
    currentExpirationDate = null;
    
    qrResult.style.display = 'none';
    qrPlaceholder.style.display = 'flex';
    resetBtn.style.display = 'none';
});
