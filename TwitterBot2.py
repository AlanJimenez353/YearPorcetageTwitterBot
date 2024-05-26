import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from requests_oauthlib import OAuth1Session  

# Carga las variables de entorno desde el archivo .env
load_dotenv()

consumer_key = os.environ.get("API_KEY")
consumer_secret = os.environ.get("API_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
bearer_token = os.environ.get("BEARER_TOKEN")

# Encabezados para la autenticación
headers = {
    "Authorization": f"Bearer {bearer_token}"
}

#--------------------------------------------------------------------------------------------------- Creacion de la ProgressBar -------------------------------------------------------------------------------------------------------------

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
        fuente= ImageFont.truetype('./Resources/Fonts/ProtestRevolution-Regular.ttf', int(alto_barra * 0.7))
        #fuente = ImageFont.truetype("arial.ttf", int(alto_barra * 0.5))  # Ajustar el tamaño de la fuente al 50% de la altura de la barra
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
    
    # Crear la ruta completa del directorio donde se guardan las imagenes
    directorio = os.path.join(os.getcwd(), "Resources", "Images")
    # Crear el directorio si no existe
    if not os.path.exists(directorio):
        os.makedirs(directorio)


    nombre_archivo = f"barra_de_carga_{porcentaje}.png"
    ruta_completa = os.path.join(directorio, nombre_archivo)
    imagen.save(ruta_completa)
    print(f"Imagen guardada como {nombre_archivo}")
    return nombre_archivo  # Asegurarse de devolver el nombre del archivo


def calcular_porcentaje_transcurrido():
    from datetime import datetime
    now = datetime.now()

    year_start = datetime(now.year, 1, 1)
    days_passed = (now - year_start).days

    total_days_in_year = (datetime(now.year + 1, 1, 1) - year_start).days

    percentage_passed = (days_passed / total_days_in_year) * 100

    return int(round(percentage_passed))

#--------------------------------------------------------------------  Manejo de archivos para guardar y leer el último porcentaje procesado ----------------------------------------------------------------------------------------------

# Guardamos el ultimo porcentaje del año guardado para que el tweet solo se envie cuando el porcentaje cambia.
def guardar_ultimo_porcentaje(porcentaje):
    with open('ultimo_porcentaje.txt', 'w') as file:
        file.write(str(porcentaje))

# Función para leer el último porcentaje procesado
def leer_ultimo_porcentaje():
    if not os.path.isfile('ultimo_porcentaje.txt'):
        return None
    with open('ultimo_porcentaje.txt', 'r') as file:
        return int(file.read())


#------------------------------------------------------------------------------------ Llamado a la API de twitter ----------------------------------------------------------------------------------------------------------------------------

def upload_media_to_twitter(file_path):
    # Utiliza las variables de autenticación correctas
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret, resource_owner_key=access_token, resource_owner_secret=access_token_secret)
    url = "https://upload.twitter.com/1.1/media/upload.json"
    with open(file_path, "rb") as file:
        files = {"media": file}
        response = oauth.post(url, files=files)
    if response.status_code == 200:
        media_id = response.json()["media_id_string"]
        return media_id
    else:
        raise Exception(f"Media upload failed: {response.status_code} {response.text}")

def tweet_with_media(media_id, text):
    # Utiliza las variables de autenticación correctas
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret, resource_owner_key=access_token, resource_owner_secret=access_token_secret)
    url = "https://api.twitter.com/2/tweets"
    payload = {
        "text": text,
        "media": {
            "media_ids": [media_id]
        }
    }
    response = oauth.post(url, json=payload)
    if response.status_code == 201:
        print("Tweet posted successfully")
    else:
        raise Exception(f"Failed to post tweet: {response.status_code} {response.text}")


#--------------------------------------------------------------------------------------------------- MAIN -------------------------------------------------------------------------------------------------------------------------------------------

try:
    # Calcula el porcentaje transcurrido del año actual
    porcentaje_transcurrido = calcular_porcentaje_transcurrido()
    # Lee el último porcentaje guardado
    porcentaje_ultimo = leer_ultimo_porcentaje()
    # Comprueba si el porcentaje ha cambiado desde la última vez
    if porcentaje_transcurrido != porcentaje_ultimo:
        # Si ha cambiado, crea la imagen de la barra de carga
        image_path = crear_barra_de_carga(porcentaje_transcurrido)
        # Sube la imagen a Twitter
        media_id = upload_media_to_twitter(image_path)
        # Define el texto del tweet
        tweet_text = f"2024 Completado en un ↓"
        # Publica el tweet con la imagen
        tweet_with_media(media_id, tweet_text)
        # Guarda el nuevo porcentaje como el último procesado
        guardar_ultimo_porcentaje(porcentaje_transcurrido)
    else:
        # Si el porcentaje no ha cambiado, cancela la ejecución para no subir imagenes repetidas
        print("El porcentaje no ha cambiado desde la última ejecución.")
except Exception as e:
    print(e)
