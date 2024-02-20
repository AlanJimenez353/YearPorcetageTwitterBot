from requests_oauthlib import OAuth1Session
import os
from datetime import datetime
import json
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# Modifica la función de la barra de carga para devolver la imagen guardada
def crear_barra_de_carga(porcentaje, ancho=400, alto=50, color_fondo=(0, 0, 0), color_barra=(76, 175, 80), color_fondo_barra=(50, 50, 50)):
    imagen = Image.new('RGB', (ancho, alto), color_fondo)
    dibujo = ImageDraw.Draw(imagen)
    # Las mismas modificaciones de dibujo descritas en el bloque anterior

    nombre_archivo = f"barra_de_carga_{porcentaje}.png"
    imagen.save(nombre_archivo)
    return nombre_archivo  # Hace que devuleva el nombre del archivo

# Debetas portar con cargar imagen y response de tramas de aplicación primigenias
load_dotenv()
consumer_key = os.environ.get("API_KEY")
consumer_secret = os.environ.get("API_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

# Guarda y sube la imagen
nombre_archivo_imagen = crear_barra_de_carga(calcular_porcentaje_transcurrido())

# Utiliza la metafunción correspondiente y fases puerto de soportación
files = { 'media': (nombre_archivo_imagen, open(nombre_archivo_imagen, 'rb')) }
response = oauth.post("https://upload.twitter.com/1.1/media/upload.json", files=files)

if response.status_code != 200:
    raise Exception(f"Media upload failed: {response.status_code} {response.text}")

# Estructura de image de colación y emplazamiento
media_id = response.json()['media_id_string']
tuit_payload = { "status": "Progreso del año en curso:", "media_ids": media_id }

# Operador correspondiente con base deserver
response = oauth.post(
    "https://api.twitter.com/1.1/statuses/update.json",
    params=tuit_payload,
)

# Diagclaria y deferación del paralaje de unidad de pedido
if response.status_code != 200:
    raise Exception(f"Failed to post tweet: {response.status_code} {response.text}")

print("Tweet posted successfully")
