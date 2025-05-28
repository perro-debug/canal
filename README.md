# Reproductor de Canales Online

Una sencilla aplicación de escritorio para reproducir canales de TV online desde un archivo M3U local.

## Requisitos

Para ejecutar esta aplicación, necesitarás:

*   **Python 3.x:** Asegúrate de tener Python 3 instalado en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/).
*   **VLC Media Player:** La aplicación VLC Media Player **debe estar instalada** en tu sistema. El reproductor utiliza libVLC, por lo que la instalación completa de VLC es necesaria. Puedes descargarlo desde [videolan.org/vlc/](https://www.videolan.org/vlc/).
*   **Biblioteca `python-vlc`:** Esta biblioteca de Python es esencial para controlar la instancia de VLC.

Opcional (para futuras funcionalidades de logos):
*   Biblioteca `Pillow`
*   Biblioteca `requests`

## Instalación de Dependencias

1.  Abre una terminal o símbolo del sistema.
2.  Instala la biblioteca `python-vlc` usando pip:
    ```bash
    pip install python-vlc
    ```
3.  (Opcional) Si se implementa la carga de logos desde URLs, instala `Pillow` y `requests`:
    ```bash
    pip install Pillow requests
    ```

## Cómo Ejecutar la Aplicación

1.  Asegúrate de tener el archivo `canales_online_lista.m3u` en el mismo directorio que el script `reproductor_video.py`.
2.  Navega hasta el directorio de la aplicación en tu terminal.
3.  Ejecuta el script:
    ```bash
    python reproductor_video.py
    ```

## Estructura del Archivo M3U

La aplicación espera un archivo llamado `canales_online_lista.m3u` ubicado en el mismo directorio que el script principal.
El formato esperado para este archivo es el estándar M3U, que consiste principalmente en pares de líneas:

*   Una línea `#EXTINF` que contiene metadatos del canal, como el nombre (extraído de `tvg-name="..."` o del texto después de la última coma).
    Ejemplo: `#EXTINF:-1 tvg-name="Nombre del Canal" tvg-logo="url_del_logo.png",Nombre del Canal`
*   Una línea con la URL del stream del canal.
    Ejemplo: `http://servidor.com/stream`

## Notas Adicionales

*   **macOS:** La reproducción de video integrada en la ventana de la aplicación en macOS podría requerir configuración manual adicional de VLC o de la biblioteca `python-vlc`. Esto se debe a cómo macOS gestiona las ventanas y la integración con VLC. Es posible que el video se reproduzca en una ventana separada o no se muestre correctamente incrustado sin ajustes específicos de la plataforma.
*   La aplicación actualmente carga los canales desde un archivo M3U local llamado `canales_online_lista.m3u`.
*   Los mensajes de estado y errores básicos se muestran en una barra de estado en la parte inferior de la ventana.

---
Desarrollado como un ejemplo de reproductor de video simple.
