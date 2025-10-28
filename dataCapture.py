import tkinter as tk
import os
import datetime
from PIL import ImageGrab
from screeninfo import get_monitors


# Create the main window
window = tk.Tk()
window.title("Data Capture")
window.geometry("200x300")

# Create a frame to hold the buttons and space them evenly
button_frame = tk.Frame(window)
button_frame.pack(expand=True)

button_width = 20
button_height = 3

# Main variable for the capturing state
is_capturing = False


# Capturing:
def capture_full_screen(directory):
    """
    Captures a full screenshot using Pillow and saves it with timestamp
    """
    # Create screenshots directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get Bounding Box
    bbox = get_selected_monitor_bbox()

    # Capture the entire screen
    screenshot = ImageGrab.grab(bbox=bbox)

    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{directory}/fullscreen_{timestamp}.jpg"

    # Resize to 360p for smaller file size
    screenshot = screenshot.resize((640, 360), ImageGrab.Image.LANCZOS)

    # Save the screenshot
    screenshot.save(filename, "JPEG")
    print(f"Screenshot saved as: {filename}")

def capture_commercial_loop():
    if is_capturing:
        capture_full_screen("training_data/commercials")
        window.after(3000, capture_commercial_loop)  # Schedule next capture

def handle_capture_commercial_press():
    global is_capturing
    is_capturing = True
    capture_commercial_button.config(state="disabled")
    capture_game_button.config(state="disabled")
    capture_commercial_button.config(bg="green")
    window.after(1000, window.iconify)  # Minimize after 1 second
    capture_commercial_loop()  # Start the loop

def capture_game_loop():
    if is_capturing:
        capture_full_screen("training_data/game")
        window.after(5000, capture_game_loop)

def handle_capture_game_press():
    global is_capturing
    is_capturing = True
    capture_commercial_button.config(state="disabled")
    capture_game_button.config(state="disabled")
    capture_game_button.config(bg="green")
    window.after(1000, window.iconify)  # Minimize after 1 second
    capture_game_loop()

def stop_capture():
    global is_capturing
    is_capturing = False
    capture_commercial_button.config(state="normal")
    capture_game_button.config(state="normal")
    capture_commercial_button.config(bg="SystemButtonFace")
    capture_game_button.config(bg="SystemButtonFace")

def on_window_deiconify(event):
    global is_capturing
    if is_capturing:
        stop_capture()

window.bind("<Map>", on_window_deiconify)

# Monitor Helpers:
def get_monitor_names(monitors):
    main_monitor_name = ""
    monitor_names = []
    for monitor in monitors:
        if (monitor.is_primary == True):
            main_monitor_name = monitor.name
        monitor_names.append(monitor.name)
    
    return monitor_names, main_monitor_name

def get_selected_monitor_bbox():
    monitors = get_monitors()
    for monitor in monitors:
        if (monitor.name == monitor_selection.get()):
            return (monitor.x, monitor.y, monitor.x + monitor.width, monitor.y + monitor.height)
    
    raise Exception("Could not find monitor to calculate bounding box.")

# Display Elements:

capture_commercial_button = tk.Button(
    button_frame,
    text="Capture Commercial",
    command=handle_capture_commercial_press,
    width=button_width,
    height=button_height
)
capture_commercial_button.pack(pady=(10, 5))  # Top margin 10, bottom margin 5

capture_game_button = tk.Button(
    button_frame,
    text="Capture Game",
    command=handle_capture_game_press,
    width=button_width,
    height=button_height
)
capture_game_button.pack(pady=5)  # Vertical spacing between buttons 

monitor_selection_label = tk.Label(window, text="Select Which Monitor To Capture").pack()

monitors = get_monitors()
monitor_names, main_monitor_name = get_monitor_names(monitors)
monitor_selection = tk.StringVar(value=main_monitor_name)
monitor_selection_dropdown = tk.OptionMenu(
    window,
    monitor_selection, 
    *monitor_names
).pack()

info_label = tk.Label(
    window,
    text="Window auto-minimizes on capture start; capturing stops when reopened.",
    wraplength=180,
    justify="center"
)
info_label.pack(pady=(15, 5))


window.mainloop()
