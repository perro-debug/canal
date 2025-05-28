# Reproductor de Canales Online

Una sencilla aplicación de escritorio para reproducir canales de TV online desde un archivo M3U local.

## Requisitos

Para ejecutar esta aplicación, necesitarás:

*   **Python 3.x:** Asegúrate de tener Python 3 instalado en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/).
*   **VLC Media Player (la aplicación completa):** Este es un requisito **mandatorio**. La aplicación `python-vlc` interactúa directamente con las bibliotecas principales de VLC Media Player. Por lo tanto, la **aplicación completa de VLC Media Player debe estar instalada** en tu sistema, no solo un conjunto de códecs o una versión ligera. Puedes descargarlo desde el sitio oficial: [https://www.videolan.org/vlc/](https://www.videolan.org/vlc/).
*   **Biblioteca `python-vlc`:** Esta biblioteca de Python es esencial para controlar la instancia de VLC desde Python.

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

## Solución de Problemas (Troubleshooting)

A continuación, se presentan algunos problemas comunes y sus posibles soluciones:

### Error: `FileNotFoundError: Could not find module 'libvlc.dll'` (o `libvlc.so`, `libvlc.dylib`)

*   **Descripción:** Este error ocurre cuando la aplicación Python no puede encontrar las bibliotecas principales de VLC (como `libvlc.dll` en Windows, `libvlc.so` en Linux, o `libvlc.dylib` en macOS).
*   **Causa Principal:** La biblioteca `python-vlc` no puede localizar una instalación válida de VLC Media Player en las rutas esperadas del sistema.

*   **Posibles Soluciones:**
    1.  **Verificar Instalación de VLC:** Asegúrate de que VLC Media Player (la aplicación completa) esté correctamente instalado en tu sistema. Si no lo está, descárgalo e instálalo desde el sitio oficial: [https://www.videolan.org/vlc/](https://www.videolan.org/vlc/).
    2.  **Coincidencia de Arquitectura (Python y VLC):** Verifica que la arquitectura de tu instalación de VLC Media Player (32-bit o 64-bit) coincida con la arquitectura de tu instalación de Python. Por ejemplo, si estás usando Python 64-bit, necesitas tener instalada la versión de VLC 64-bit. Si usas Python 32-bit, necesitas VLC 32-bit. Esta es una causa común de problemas.
    3.  **Reinstalación Completa de VLC:** Considera desinstalar VLC Media Player por completo y luego reinstalarlo. Durante la instalación, asegúrate de que todos los componentes necesarios estén seleccionados (a veces pueden aparecer como "plugins", "componentes de desarrollo", "librerías" o similar, aunque la instalación estándar suele incluir todo lo necesario).
    4.  **(Avanzado) Variable de Entorno `PATH`:** En raras ocasiones, puede ser necesario agregar el directorio de instalación de VLC a la variable de entorno `PATH` de tu sistema.
        *   Por ejemplo, en Windows, si VLC está instalado en `C:\Program Files\VideoLAN\VLC`, podrías agregar esta ruta al `PATH`.
        *   Esto generalmente no es requerido, ya que la biblioteca `python-vlc` está diseñada para encontrar automáticamente las instalaciones de VLC en las ubicaciones más comunes. Procede con esta opción con precaución.
