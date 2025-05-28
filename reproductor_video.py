import tkinter as tk
import vlc
import sys

# Create the main window
root = tk.Tk()
root.title("Reproductor de Canales Online")

# Global variable to store the name of the currently playing channel
current_channel_name = ""

# --- M3U Parsing Logic ---
import re

def parse_m3u(filepath):
    """
    Parses an M3U file and extracts channel information.

    Args:
        filepath (str): The path to the M3U file.

    Returns:
        list: A list of dictionaries, where each dictionary contains
              the 'name', 'logo', and 'url' for a channel.
              Returns an empty list if the file cannot be read.
    """
    channels = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("#EXTINF"):
                name = ""
                logo = ""
                url = ""

                # Try to extract tvg-name and tvg-logo using regex
                tvg_name_match = re.search(r'tvg-name="([^"]*)"', line)
                if tvg_name_match and tvg_name_match.group(1):
                    name = tvg_name_match.group(1)

                tvg_logo_match = re.search(r'tvg-logo="([^"]*)"', line)
                if tvg_logo_match:
                    logo = tvg_logo_match.group(1)

                # If tvg-name was not found or empty, get name from the end of the line
                if not name:
                    parts = line.split(',')
                    if len(parts) > 1:
                        name = parts[-1].strip()

                # The next line should be the URL
                if i + 1 < len(lines):
                    next_line = lines[i+1].strip()
                    if next_line and not next_line.startswith("#"):
                        url = next_line
                        i += 1 # Move past the URL line

                if name and url:
                    channels.append({"name": name, "logo": logo, "url": url})
            i += 1
    except FileNotFoundError:
        print(f"Error: M3U file not found at {filepath}")
        return []
    except IOError as e:
        print(f"Error reading M3U file {filepath}: {e}")
        return []
    return channels

# (Code for parsing M3U files will go here)

# --- UI Elements ---
root.geometry("800x600") # Set initial window size

# Create main frames
frame_controls = tk.Frame(root)
frame_controls.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

frame_main_content = tk.Frame(root)
frame_main_content.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

frame_channels = tk.Frame(frame_main_content, width=200)
frame_channels.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
frame_channels.pack_propagate(False) # Prevent frame from shrinking to fit content

frame_video = tk.Frame(frame_main_content, bg="black") # Placeholder for video
frame_video.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

# Channel Listbox
listbox_channels_scrollbar = tk.Scrollbar(frame_channels, orient=tk.VERTICAL)
listbox_channels = tk.Listbox(frame_channels, yscrollcommand=listbox_channels_scrollbar.set, width=30)
listbox_channels_scrollbar.config(command=listbox_channels.yview)
listbox_channels_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox_channels.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Populate Channel Listbox
# Make parsed_channels globally accessible for the event handler
global_parsed_channels = [] 

def populate_channel_listbox():
    global global_parsed_channels, current_channel_name
    update_status("Cargando lista de canales...")
    listbox_channels.delete(0, tk.END) # Clear existing items first
    parsed_data = parse_m3u('canales_online_lista.m3u') # Renamed to avoid conflict
    if parsed_data:
        global_parsed_channels = parsed_data
        for channel_item in global_parsed_channels: # Renamed to avoid conflict
            listbox_channels.insert(tk.END, channel_item.get("name", "Nombre Desconocido"))
        update_status("Lista de canales cargada.")
    else:
        global_parsed_channels = [] # Ensure it's empty
        listbox_channels.insert(tk.END, "No se pudieron cargar los canales.")
        update_status("Error al cargar la lista de canales.")

populate_channel_listbox() # Initial population

def on_channel_select(event):
    """Handles channel selection in the listbox."""
    global current_channel_name
    selected_indices = listbox_channels.curselection()
    if not selected_indices:
        return

    selected_index = selected_indices[0]
    if global_parsed_channels and 0 <= selected_index < len(global_parsed_channels):
        channel = global_parsed_channels[selected_index]
        url = channel.get("url")
        current_channel_name = channel.get("name", "Nombre Desconocido") # Store current channel name
        if url:
            update_status(f"Cargando canal: {current_channel_name}...")
            print(f"Selected channel: {current_channel_name}, URL: {url}")
            load_video(url)
            # Play will be handled by VLC event or load_video can call play_video if needed
            # For now, let's assume play_video is called after load_video or by an event
            play_video() 
        else:
            update_status(f"No URL para: {current_channel_name}")
            print(f"No URL found for selected channel: {current_channel_name}")

listbox_channels.bind('<<ListboxSelect>>', on_channel_select)

# Video Display Placeholder (alternative: Label)
# label_video_placeholder = tk.Label(frame_video, text="Área de Video", bg="black", fg="white") # Removed
# label_video_placeholder.pack(expand=True, fill=tk.BOTH)                                     # Removed


# Playback Controls
btn_play_pause = tk.Button(frame_controls, text="Reproducir/Pausar", command=pause_video)
btn_play_pause.pack(side=tk.LEFT, padx=5, pady=5)

btn_stop = tk.Button(frame_controls, text="Detener", command=stop_video)
btn_stop.pack(side=tk.LEFT, padx=5, pady=5)

# --- Video Playback Logic ---
# VLC setup
vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()

# Ensure frame_video is updated before getting its ID for VLC
root.update_idletasks() 

# Embed video player into frame_video
if sys.platform.startswith('linux'):
    try:
        player.set_xwindow(frame_video.winfo_id())
    except Exception as e:
        print(f"Error setting xwindow: {e}")
elif sys.platform.startswith('win32'):
    try:
        player.set_hwnd(frame_video.winfo_id())
    except Exception as e:
        print(f"Error setting hwnd: {e}")
elif sys.platform.startswith('darwin'): # macOS
    try:
        # For macOS, libVLC version 3.x needs to set an NSView
        # This requires a bit more setup, often involving a library like `ctypes`
        # to pass the NSView pointer. For now, we'll print a message.
        # from ctypes import c_void_p, cast
        # player.set_nsobject(cast(frame_video.winfo_id(), c_void_p))
        print("Playback on macOS might require additional setup for video embedding.")
        # As a fallback, try to set the window ID directly, though it might not work as expected for video.
        player.set_hwnd(frame_video.winfo_id()) # This is not ideal for macOS video but better than nothing
    except Exception as e:
        print(f"Error setting nsobject/hwnd for macOS: {e}")
else:
    print(f"Unsupported platform: {sys.platform}. Video embedding might not work.")


def load_video(url):
    """Loads a video from a URL into the VLC player."""
    if not url:
        print("Error: No URL provided to load_video.")
        return
    try:
        media = vlc_instance.media_new(url)
        player.set_media(media)
        print(f"Media loaded: {url}")
    except Exception as e:
        print(f"Error loading media {url}: {e}")

def play_video():
    """Plays the currently loaded video."""
    try:
        print("Attempting to play video...")
        player.play()
    except Exception as e:
        print(f"Error playing video: {e}")

def pause_video():
    """Pauses or resumes the currently playing video."""
    try:
        print("Attempting to pause/resume video...")
        player.pause() # Toggles pause state
    except Exception as e:
        print(f"Error pausing/resuming video: {e}")

def stop_video():
    """Stops the currently playing video."""
    try:
        print("Attempting to stop video...")
        player.stop()
    except Exception as e:
        print(f"Error stopping video: {e}")

# (Code for handling video playback using a library like VLC or ffpyplayer will go here)

# Status Bar
status_bar_label = tk.Label(root, text="Bienvenido", relief=tk.SUNKEN, anchor=tk.W)
status_bar_label.pack(side=tk.BOTTOM, fill=tk.X)

def update_status(message):
    """Updates the status bar text."""
    if status_bar_label:
        status_bar_label.config(text=message)
        print(f"Status: {message}") # Also print to console for debugging

# VLC Event Handlers
def handle_vlc_playing(event):
    global current_channel_name
    update_status(f"Reproduciendo: {current_channel_name}")

def handle_vlc_error(event):
    global current_channel_name
    update_status(f"Error al reproducir: {current_channel_name}")

def handle_vlc_buffering(event, player_instance): # player_instance is passed by vlc.py
    # The event itself doesn't contain the buffering percentage in older python-vlc versions directly with this callback signature
    # We might need to query player.get_state() or look at event.u.media_player_buffering.new_cache
    # For simplicity, just indicate buffering.
    # new_cache = event.u.media_player_buffering.new_cache # This is how you'd get it with correct event setup
    # update_status(f"Cargando buffer ({new_cache}%): {current_channel_name}...")
    
    # The event object for MediaBuffering has a 'u' union, and inside that, 'media_player_buffering'
    # which contains 'new_cache' (a float representing the buffer percentage).
    # However, the callback registered with event_attach for some simple events might not directly pass the full event object
    # or the structure might be tricky. Let's get the percentage from the player if possible.
    
    # The event itself is just a notification. We query the player for the cache value.
    # The event structure 'event.u.media_player_buffering.new_cache' is the correct way for some VLC events,
    # but let's try a simpler message first as getting the value might be complex depending on python-vlc version
    # and how events are handled.
    
    # The event argument for MediaPlayerBuffering is actually the new cache value (a float).
    # event_type, callback, *args (player_instance is one of those args if provided during attach)
    # The `event` parameter itself for MediaPlayerBuffering should be the vlc.Event object
    # which has `event.u.media_player_buffering.new_cache`.
    
    # Let's assume `event` is the vlc.Event object.
    buffer_percentage = event.u.media_player_buffering.new_cache
    update_status(f"Cargando buffer ({buffer_percentage:.0f}%): {current_channel_name}...")


# Attach VLC Events
event_manager = player.event_manager()
event_manager.event_attach(vlc.EventType.MediaPlayerPlaying, handle_vlc_playing)
event_manager.event_attach(vlc.EventType.MediaPlayerEncounteredError, handle_vlc_error)
# For MediaPlayerBuffering, the callback receives the event object.
event_manager.event_attach(vlc.EventType.MediaPlayerBuffering, handle_vlc_buffering)


# Start the Tkinter event loop
update_status("Aplicación iniciada. Seleccione un canal.") # Initial status
root.mainloop()
