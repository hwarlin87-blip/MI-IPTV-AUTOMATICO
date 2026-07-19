import requests
import re

def obtener_enlace_dinamico(url_web, patron_regex):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url_web, headers=headers, timeout=10)
        # Busca el enlace oculto (.m3u8) dentro del código de la página web
        match = re.search(patron_regex, response.text)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"Error buscando en {url_web}: {e}")
    return None

# --- CONFIGURACIÓN DE TUS CANALES ---
# Aquí pondremos las páginas web oficiales de tus canales dominicanos
canales_actualizados = {}

# Ejemplo para Colorvisión Canal 9 (Buscamos su señal oficial)
enlace_colorvision = obtener_enlace_dinamico(
    "https://colorvision.com.do/en-vivo/", 
    r'(https://[^"\']*?playlist\.m3u8[^"\']*?)'
)
if enlace_colorvision:
    canales_actualizados["Colorvision 9"] = enlace_colorvision

# --- AQUÍ EL ROBOT ESCRIBE TU ARCHIVO LISTA.M3U8 ---
# Volvemos a armar tu archivo m3u8 con los enlaces nuevos que encontró
m3u8_contenido = "#EXTM3U\n"

# Canal 9 (Se actualiza solo)
if "Colorvision 9" in canales_actualizados:
    m3u8_contenido += '#EXTINF:-1 group-title="News" tvg-logo="https://encrypted-tbn0.gstatic.com",Colorvision 9\n'
    m3u8_contenido += f'{canales_actualizados["Colorvision 9"]}\n'
else:
    # Si el robot falla, deja el que tenías por defecto
    m3u8_contenido += '#EXTINF:-1 group-title="News" tvg-logo="https://encrypted-tbn0.gstatic.com",Colorvision 9\n'
    m3u8_contenido += 'https://live.eu-north-1a.cf.dmcdn.net/sec(55BNqf.../live_480.m3u8\n'

# (Aquí abajo agregaríamos los demás canales uno por uno...)

# Guardar los cambios en el archivo que lee tu tele
with open("lista.m3u8", "w", encoding="utf-8") as f:
    f.write(m3u8_contenido)

print("¡Lista de canales actualizada con éxito por el Robot!")
