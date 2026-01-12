import qrcode
from datetime import datetime, timedelta
import json
import os

def generar_qr_con_expiracion(url, nombre_archivo="qr_code.png", meses=12):
    """
    Genera un código QR con información de expiración en formato JSON
    
    IMPORTANTE: El QR contendrá un JSON con la URL y las fechas. 
    Necesitarás una aplicación personalizada que lea este JSON y 
    valide la fecha antes de abrir el link. El QR por sí mismo NO expirará.
    
    Args:
        url (str): El link que quieres convertir a QR
        nombre_archivo (str): Nombre del archivo de salida (default: qr_code.png)
        meses (int): Meses hasta la expiración (default: 12)
    """
    # Calcular fecha de expiración
    fecha_expiracion = datetime.now() + timedelta(days=30 * meses)
    
    # Crear datos del QR con la URL y fecha de expiración
    datos_qr = {
        "url": url,
        "expira": fecha_expiracion.strftime("%Y-%m-%d %H:%M:%S"),
        "creado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Convertir a JSON para incluir en el QR
    contenido_qr = json.dumps(datos_qr, ensure_ascii=False)
    
    # Configurar el generador de QR
    qr = qrcode.QRCode(
        version=1,  # Tamaño del QR (1-40)
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # Tamaño de cada caja en píxeles
        border=4,  # Grosor del borde
    )
    
    # Agregar datos al QR
    qr.add_data(contenido_qr)
    qr.make(fit=True)
    
    # Crear la imagen
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Guardar la imagen
    img.save(nombre_archivo)
    
    print(f"\n✓ Código QR generado exitosamente: {nombre_archivo}")
    print(f"✓ URL: {url}")
    print(f"✓ Fecha de creación: {datos_qr['creado']}")
    print(f"✓ Fecha de expiración: {datos_qr['expira']}")
    print(f"\n⚠️  IMPORTANTE:")
    print(f"   Este QR contiene un JSON con la URL y las fechas.")
    print(f"   Necesitas una app que valide la fecha de expiración.")
    print(f"   El QR por sí mismo NO expirará automáticamente.\n")
    
    return nombre_archivo


def generar_qr_simple(url, nombre_archivo="qr_simple.png", meses=12):
    """
    Genera un código QR simple solo con la URL
    
    IMPORTANTE: Los códigos QR son imágenes estáticas que NO expiran automáticamente.
    La fecha de expiración es solo una referencia para ti. Para expiración real,
    considera usar servicios de acortamiento de URLs con expiración (Bitly, TinyURL).
    
    Args:
        url (str): El link que quieres convertir a QR
        nombre_archivo (str): Nombre del archivo de salida
        meses (int): Meses hasta la expiración (solo informativo, default: 12)
    """
    # Crear QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # Crear la imagen
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Guardar la imagen
    img.save(nombre_archivo)
    
    # Calcular fecha de expiración (solo informativa)
    fecha_expiracion = datetime.now() + timedelta(days=30 * meses)
    
    print(f"\n✓ Código QR generado exitosamente: {nombre_archivo}")
    print(f"✓ URL: {url}")
    print(f"✓ Fecha de referencia de expiración: {fecha_expiracion.strftime('%Y-%m-%d')}")
    print(f"\n⚠️  IMPORTANTE:")
    print(f"   Los códigos QR NO expiran automáticamente.")
    print(f"   Este QR funcionará siempre mientras la URL sea válida.")
    print(f"   La fecha es solo una referencia para tu control.\n")
    print(f"💡 TIP: Para expiración real, usa un acortador de URLs como:")
    print(f"   - Bitly (bitly.com)")
    print(f"   - TinyURL (tinyurl.com)")
    print(f"   Y luego genera el QR del link corto.\n")
    
    return nombre_archivo


if __name__ == "__main__":
    try:
        print("╔═══════════════════════════════════════════════╗")
        print("║    🎯 Generador de Códigos QR con Expiración  ║")
        print("╚═══════════════════════════════════════════════╝\n")
        
        # Solicitar URL al usuario
        url = input("📎 Ingresa el link/URL: ").strip()
        
        if not url:
            print("❌ Error: Debes ingresar una URL válida")
            exit(1)
        
        # Preguntar meses de expiración
        print("\n⏰ ¿Cuántos meses hasta la expiración?")
        meses_input = input("   (Enter para 12 meses): ").strip()
        meses = int(meses_input) if meses_input.isdigit() else 12
        
        # Preguntar tipo de QR
        print("\n📋 ¿Qué tipo de QR deseas generar?")
        print("   1. QR Simple (solo URL)")
        print("   2. QR con Metadata (incluye fechas en JSON)")
        opcion = input("\n   Selecciona una opción (1/2): ").strip()
        
        if opcion == "1":
            nombre = input("\n💾 Nombre del archivo (Enter para 'qr_simple.png'): ").strip()
            if not nombre:
                nombre = "qr_simple.png"
            elif not nombre.endswith('.png'):
                nombre += '.png'
            
            generar_qr_simple(url, nombre, meses)
            
        elif opcion == "2":
            nombre = input("\n💾 Nombre del archivo (Enter para 'qr_metadata.png'): ").strip()
            if not nombre:
                nombre = "qr_metadata.png"
            elif not nombre.endswith('.png'):
                nombre += '.png'
            
            generar_qr_con_expiracion(url, nombre, meses)
            
        else:
            print("❌ Opción no válida")
            exit(1)
            
    except Exception as e:
        print(f"\n❌ Error al generar el QR: {e}")
        print("\n💡 Asegúrate de tener instaladas las dependencias:")
        print("   pip install qrcode[pil]")
        exit(1)
