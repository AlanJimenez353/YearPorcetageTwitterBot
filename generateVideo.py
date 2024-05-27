import os
from moviepy.editor import ImageSequenceClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip

def leer_ultimo_porcentaje(archivo):
    if not os.path.exists(archivo):
        print(f"El archivo {archivo} no existe. Creando un archivo con el valor predeterminado de 1.")
        with open(archivo, 'w') as file:
            file.write('1')
        return 1
    with open(archivo, 'r') as file:
        return int(file.read().strip())

def calcular_duraciones_progresivas(num_imagenes, duracion_total, num_lentas=8):
    """
    Calcula una lista de duraciones para cada frame, con las primeras imágenes pasando rápido y las últimas num_lentas imágenes más lentamente.
    """
    if num_imagenes <= 0:
        return []

    num_lentas = min(num_lentas, num_imagenes)
    num_rapidas = num_imagenes - num_lentas

    # Duración total de las imágenes rápidas y lentas
    duracion_rapida_total = duracion_total * 0.5
    duracion_lenta_total = duracion_total * 0.5

    # Duraciones para imágenes rápidas
    duracion_rapida_por_imagen = duracion_rapida_total / max(1, num_rapidas)
    duraciones_rapidas = [duracion_rapida_por_imagen] * num_rapidas

    # Duraciones para imágenes lentas
    duracion_lenta_por_imagen = duracion_lenta_total / max(1, num_lentas)
    duraciones_lentas = [duracion_lenta_por_imagen] * num_lentas

    # Combinando las duraciones
    duraciones = duraciones_rapidas + duraciones_lentas

    return duraciones

def crear_video_barra_progreso(directorio_imagenes, archivo_porcentaje, archivo_salida_base, archivo_audio, duracion_total=8, fps=24):
    # Leer el último porcentaje del archivo
    print(f"Archivo porcentaje: {archivo_porcentaje}")
    ultimo_porcentaje = leer_ultimo_porcentaje(archivo_porcentaje)
    
    # Obtener la lista de archivos de imagen correspondientes a los porcentajes
    imagenes = [os.path.join(directorio_imagenes, f"barra_de_carga_{i}.png") for i in range(1, ultimo_porcentaje + 1)]
    
    # Verificar que las imágenes existen
    for img in imagenes:
        if not os.path.exists(img):
            raise FileNotFoundError(f"La imagen {img} no existe.")
        print(f"Imagen encontrada: {img}")
    
    # Calcular duraciones progresivas para cada imagen
    duraciones = calcular_duraciones_progresivas(len(imagenes), duracion_total)
    
    # Crear el video a partir de la secuencia de imágenes y duraciones
    clips = [ImageSequenceClip([img], durations=[dur]) for img, dur in zip(imagenes, duraciones)]
    
    # Concatenar los clips
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # Agregar el audio
    if os.path.exists(archivo_audio):
        audio_clip = AudioFileClip(archivo_audio)
        audio_duration = audio_clip.duration
        audio_clips = [audio_clip.set_start(sum(duraciones[:i])) for i in range(len(duraciones))]
        concatenated_audio = CompositeAudioClip(audio_clips)
        final_clip = final_clip.set_audio(concatenated_audio)
    else:
        print(f"El archivo de audio {archivo_audio} no existe.")
    
    # Crear el nombre del archivo de salida incluyendo el último porcentaje
    archivo_salida = f"{archivo_salida_base}_{ultimo_porcentaje}.mp4"
    
    # Crear el directorio de salida si no existe
    os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)
    
    # Escribir el video en el archivo de salida
    final_clip.write_videofile(archivo_salida, codec="libx264", fps=fps)

# Ruta al directorio donde están almacenadas las imágenes
directorio_imagenes = os.path.join(os.getcwd(), "Resources", "Images")

# Ruta al archivo donde está guardado el último porcentaje generado
archivo_porcentaje = os.path.join("C:\\Users\\Alan\\Desktop\\TwitterBot", "ultimo_porcentaje.txt")

# Base del nombre del archivo de salida del video
directorio_videos = os.path.join(os.getcwd(), "Resources", "videos")
archivo_salida_base = os.path.join(directorio_videos, "barra_progreso")

# Ruta al archivo de audio para la transición
archivo_audio = os.path.join("C:\\Users\\Alan\\Desktop\\TwitterBot\\Resources\\Sounds", "67610__qubodup__metal_click_6.flac")

# Crear el video
crear_video_barra_progreso(directorio_imagenes, archivo_porcentaje, archivo_salida_base, archivo_audio)
