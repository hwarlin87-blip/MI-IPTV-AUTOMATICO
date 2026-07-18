import requests

def generar_m3u():
    # URL de la API oficial de Pluto TV para canales en español
    url_api = "https://api.pluto.tv/v2/channels"
    
    try:
        response = requests.get(url_api)
        channels = response.json()
        
        # Iniciamos el archivo M3U8
        m3u_content = "#EXTM3U\n"
        
        for channel in channels:
            name = channel.get('name', 'Canal Sin Nombre')
            category = channel.get('category', 'Variados')
            logo = ""
            
            # Buscamos el logo del canal si existe
            if channel.get('images'):
                logo = channel['images'][0].get('url', '')
                
            # Buscamos la URL del stream de video (M3U8)
            # Nota: Pluto usa urls dinámicas que este script lee en tiempo real
            stream_url = channel.get('stitcherParams', {}).get('url', '')
            
            if not stream_url and channel.get('streams'):
                stream_url = channel['streams'][0].get('url', '')
                
            if stream_url:
                m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{category}",{name}\n'
                m3u_content += f'{stream_url}\n'
                
        # Guardamos el archivo final
        with open("lista_automatica.m3u8", "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print("¡Lista M3U8 actualizada con éxito!")
        
    except Exception as e:
        print(f"Error al generar la lista: {e}")

if __name__ == "__main__":
    generar_m3u()
