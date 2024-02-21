import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from requests_oauthlib import OAuth1Session  # Asegúrate de haber instalado requests_oauthlib

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
    return nombre_archivo  # Retorna el nombre del archivo

def calcular_porcentaje_transcurrido():
    from datetime import datetime
    now = datetime.now()

    year_start = datetime(now.year, 1, 1)
    days_passed = (now - year_start).days

    total_days_in_year = (datetime(now.year + 1, 1, 1) - year_start).days

    percentage_passed = (days_passed / total_days_in_year) * 100

    return int(round(percentage_passed))













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

try:
    porcentaje_transcurrido = calcular_porcentaje_transcurrido()
    image_path = crear_barra_de_carga(porcentaje_transcurrido)
    media_id = upload_media_to_twitter(image_path)
    tweet_text = "Hola mundo, este es un tweet automatizado con imagen."
    tweet_with_media(media_id, tweet_text)
except Exception as e:
    print(e)
