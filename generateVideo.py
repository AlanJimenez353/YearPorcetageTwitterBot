import os
from moviepy.editor import (
    ImageSequenceClip,
    concatenate_videoclips,
    AudioFileClip,
    CompositeAudioClip,
    TextClip,
    ColorClip,
    vfx
)
from moviepy.config import change_settings

# Cambia la ruta a la instalación de ImageMagick en tu sistema
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

def leer_ultimo_porcentaje(archivo):
    if not os.path.exists(archivo):
        print(f"El archivo {archivo} no existe. Creando un archivo con el valor predeterminado de 1.")
        with open(archivo, 'w') as file:
            file.write('1')
        return 1
    with open(archivo, 'r') as file:
        return int(file.read().strip())

def calcular_duraciones_progresivas(num_imagenes, duracion_total, num_lentas=8):
    if num_imagenes <= 0:
        return []

    num_lentas = min(num_lentas, num_imagenes)
    num_rapidas = num_imagenes - num_lentas

    duracion_rapida_total = duracion_total * 0.5
    duracion_lenta_total = duracion_total * 0.5

    duracion_rapida_por_imagen = duracion_rapida_total / max(1, num_rapidas)
    duraciones_rapidas = [duracion_rapida_por_imagen] * num_rapidas

    duracion_lenta_por_imagen = duracion_lenta_total / max(1, num_lentas)
    duraciones_lentas = [duracion_lenta_por_imagen] * num_lentas

    duraciones = duraciones_rapidas + duraciones_lentas

    return duraciones

def crear_video_texto(texto, duracion, tamano, color_fondo, color_texto, fuente, fontsize=100, fps=24):
    text_clip = TextClip(texto, fontsize=fontsize, color=color_texto, font=fuente, size=tamano, bg_color=color_fondo, method='caption')
    text_clip = text_clip.set_duration(duracion).set_fps(fps)
    
    # Aplicar efectos
    text_clip = text_clip.fadein(1).fadeout(1)  # Desvanecer al inicio y al final
    text_clip = text_clip.set_position(('center', 'center'))  # Centrar el texto
    text_clip = text_clip.crossfadein(1)  # Efecto de transición

    # Efecto de movimiento (de abajo hacia arriba)
    text_clip = text_clip.set_position(lambda t: ('center', max(0, 720 - 720 * t / duracion)))
    
    return text_clip

def crear_video_barra_progreso(directorio_imagenes, archivo_porcentaje, archivo_salida_base, archivo_audio, duracion_total=8, fps=24):
    print(f"Archivo porcentaje: {archivo_porcentaje}")
    ultimo_porcentaje = leer_ultimo_porcentaje(archivo_porcentaje)
    
    imagenes = [os.path.join(directorio_imagenes, f"barra_de_carga_{i}.png") for i in range(1, ultimo_porcentaje + 1)]
    
    for img in imagenes:
        if not os.path.exists(img):
            raise FileNotFoundError(f"La imagen {img} no existe.")
        print(f"Imagen encontrada: {img}")
    
    duraciones = calcular_duraciones_progresivas(len(imagenes), duracion_total)
    
    clips = [ImageSequenceClip([img], durations=[dur]) for img, dur in zip(imagenes, duraciones)]
    
    final_clip = concatenate_videoclips(clips, method="compose")
    
    if os.path.exists(archivo_audio):
        audio_clip = AudioFileClip(archivo_audio)
        audio_duration = audio_clip.duration
        audio_clips = [audio_clip.set_start(sum(duraciones[:i])) for i in range(len(duraciones))]
        concatenated_audio = CompositeAudioClip(audio_clips)
        final_clip = final_clip.set_audio(concatenated_audio)
    else:
        print(f"El archivo de audio {archivo_audio} no existe.")
    
    archivo_salida = f"{archivo_salida_base}_{ultimo_porcentaje}.mp4"
    
    os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)
    
    final_clip.write_videofile(archivo_salida, codec="libx264", fps=fps)
    
    return final_clip

# Ejemplo de uso de una fuente preinstalada (Chiller)
fuente_preinstalada = "Chiller"

# Crear video introductorio con fuente más grande
tamano_video = (1280, 720)
video_intro = crear_video_texto("2024 is moving", duracion=3, tamano=tamano_video, color_fondo='black', color_texto='white', fuente=fuente_preinstalada, fontsize=120)

# Crear video de la barra de progreso
directorio_imagenes = os.path.join(os.getcwd(), "Resources", "Images")
archivo_porcentaje = os.path.join("C:\\Users\\Alan\\Desktop\\TwitterBot", "ultimo_porcentaje.txt")
directorio_videos = os.path.join(os.getcwd(), "Resources", "videos")
archivo_salida_base = os.path.join(directorio_videos, "barra_progreso")
archivo_audio = os.path.join("C:\\Users\\Alan\\Desktop\\TwitterBot\\Resources\\Sounds", "67610__qubodup__metal_click_6.flac")

video_barra_progreso = crear_video_barra_progreso(directorio_imagenes, archivo_porcentaje, archivo_salida_base, archivo_audio)

# Crear video final con texto "¿Are you?" con fuente más grande
video_final_text = crear_video_texto("¿ Are you ?", duracion=3, tamano=tamano_video, color_fondo='black', color_texto='white', fuente=fuente_preinstalada, fontsize=120)

# Crear un clip de color negro de 2 segundos
clip_negro = ColorClip(size=tamano_video, color=(0, 0, 0), duration=2)

# Concatenar videos
video_final = concatenate_videoclips([video_intro, video_barra_progreso, video_final_text, clip_negro], method="compose")
video_final.write_videofile(os.path.join(directorio_videos, "video_final.mp4"), codec="libx264", fps=24)
