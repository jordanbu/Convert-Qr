# Generador de Códigos QR

Aplicación web para generar códigos QR con fecha de expiración informativa.

## Características

- Generación de códigos QR a partir de URLs
- Configuración de fecha de expiración (solo informativa)
- Ajuste de tamaño del código QR
- Opción de incluir metadata en formato JSON
- Descarga del código QR generado
- Interfaz limpia y responsive

## Despliegue en Vercel

### Opción 1: Desde la línea de comandos

1. Instala Vercel CLI:
```bash
npm install -g vercel
```

2. Inicia sesión:
```bash
vercel login
```

3. Despliega:
```bash
vercel
```

### Opción 2: Desde GitHub

1. Sube el proyecto a un repositorio de GitHub
2. Ve a [vercel.com](https://vercel.com)
3. Haz clic en "Import Project"
4. Selecciona tu repositorio
5. Haz clic en "Deploy"

## Estructura del proyecto

```
├── index.html      # Página principal
├── styles.css      # Estilos
├── app.js          # Lógica de la aplicación
├── vercel.json     # Configuración de Vercel
└── README.md       # Este archivo
```

## Tecnologías

- HTML5
- CSS3
- JavaScript (Vanilla)
- QRCode.js

## Nota importante

Los códigos QR generados no expiran automáticamente. La fecha de expiración es solo informativa. Para expiración real, usa servicios de acortamiento de URLs con expiración (Bitly, TinyURL, etc.).
