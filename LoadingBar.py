from PIL import Image, ImageDraw, ImageFont

def calcular_porcentaje_transcurrido():
    from datetime import datetime
    now = datetime.now()

    year_start = datetime(now.year, 1, 1)
    days_passed = (now - year_start).days

    total_days_in_year = (datetime(now.year + 1, 1, 1) - year_start).days

    percentage_passed = (days_passed / total_days_in_year) * 100

    return int(round(percentage_passed))


from PIL import Image, ImageDraw, ImageFont

def crear_barra_de_carga(porcentaje, ancho=1024, alto=576, color_fondo=(0, 0, 0), color_barra=(76, 175, 80), color_fondo_barra=(50, 50, 50), color_borde=(3, 14, 84)):
    imagen = Image.new('RGB', (ancho, alto), color_fondo)
    dibujo = ImageDraw.Draw(imagen)

    # Aumentar la altura de la barra de progreso para que sea más prominente
    ancho_barra = int(ancho * 0.8)  # Mantiene el 80% del ancho para la barra
    alto_barra = int(alto * 0.2)  # Aumenta la altura de la barra al 20% del alto de la imagen
    margen_x = (ancho - ancho_barra) // 2
    margen_y = (alto - alto_barra) // 2

    # Dibujar el borde de la barra de carga
    grosor_borde = 2  # Definir el grosor del borde
    dibujo.rectangle([margen_x - grosor_borde, margen_y - grosor_borde, margen_x + ancho_barra + grosor_borde, margen_y + alto_barra + grosor_borde], outline=color_borde, width=grosor_borde)

    # Dibujar el fondo de la barra de carga
    dibujo.rectangle([margen_x, margen_y, margen_x + ancho_barra, margen_y + alto_barra], fill=color_fondo_barra)

    # Dibujar la barra de progreso
    ancho_barra_llena = int((porcentaje / 100) * ancho_barra)
    dibujo.rectangle([margen_x, margen_y, margen_x + ancho_barra_llena, margen_y + alto_barra], fill=color_barra)

    # Cargar la fuente
    try:
        fuente = ImageFont.truetype("arial.ttf", int(alto_barra * 0.9))  # Ajustar el tamaño de la fuente al 50% de la altura de la barra
    except IOError:
        print("No se pudo cargar la fuente personalizada. Usando la predeterminada.")
        fuente = ImageFont.load_default()

    # Dibujar el texto del porcentaje en la barra
    texto = f"{porcentaje}%"
    w, h = dibujo.textbbox((0, 0), texto, font=fuente)[2:]
    posicion_x_texto = margen_x + (ancho_barra - w) / 2
    posicion_y_texto = margen_y + (alto_barra - h) / 2
    dibujo.text((posicion_x_texto, posicion_y_texto), texto, fill="white", font=fuente)

    # Guardar la imagen con el nombre de archivo correspondiente al porcentaje
    nombre_archivo = f"barra_de_carga_{porcentaje}.png"
    imagen.save(nombre_archivo)
    print(f"Imagen guardada como {nombre_archivo}")
    return nombre_archivo  # Asegurarse de devolver el nombre del archivo



# Ejemplo de uso
crear_barra_de_carga(15)
