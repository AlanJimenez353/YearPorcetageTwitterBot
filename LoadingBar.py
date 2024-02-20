from PIL import Image, ImageDraw, ImageFont

def calcular_porcentaje_transcurrido():
    from datetime import datetime
    now = datetime.now()

    year_start = datetime(now.year, 1, 1)
    days_passed = (now - year_start).days

    total_days_in_year = (datetime(now.year + 1, 1, 1) - year_start).days

    percentage_passed = (days_passed / total_days_in_year) * 100

    return int(round(percentage_passed))


def crear_barra_de_carga(porcentaje, ancho=400, alto=50, color_fondo=(0, 0, 0), color_barra=(76, 175, 80), color_fondo_barra=(50, 50, 50)):
    imagen = Image.new('RGB', (ancho, alto), color_fondo)
    dibujo = ImageDraw.Draw(imagen)

    # Dibuja el cuadrado negro de fondo para la barra de carga
    margen = 5  # Margen entre el cuadrado de fondo y la barra de carga
    dibujo.rectangle([margen, margen, ancho - margen, alto - margen], fill=color_fondo_barra)

    ancho_barra = (porcentaje / 100) * (ancho - 2 * margen)
    posicion_barra_y = margen
    altura_barra = alto - 2 * margen
    dibujo.rectangle([margen, posicion_barra_y, margen + ancho_barra, posicion_barra_y + altura_barra], fill=color_barra)

    # Intenta cargar una fuente; si falla, usa la fuente predeterminada
    try:
        fuente = ImageFont.truetype("arial.ttf", 15)  # Ajusta el nombre de la fuente y tamaño según necesites
    except IOError:
        fuente = ImageFont.load_default()

    texto = f"{porcentaje}%"
    # Usa getbbox para obtener el cuadro delimitador del texto
    caja_texto = fuente.getbbox(texto)
    ancho_texto = caja_texto[2] - caja_texto[0]
    alto_texto = caja_texto[3] - caja_texto[1]
    posicion_x = (ancho - ancho_texto) / 2
    posicion_y = (alto - alto_texto) / 2
    dibujo.text((posicion_x, posicion_y), texto, fill="white", font=fuente)

    nombre_archivo = f"barra_de_carga_{porcentaje}.png"
    imagen.save(nombre_archivo)
    print(f"Imagen guardada como {nombre_archivo}")

# Ejemplo de uso
porcentaje_transcurrido = calcular_porcentaje_transcurrido()

crear_barra_de_carga(porcentaje_transcurrido)
