import tkinter as tk
import os
import datetime
from PIL import ImageGrab

# Create the main window
window = tk.Tk()
window.title("Data Capture")
window.geometry("200x350")

# Create a frame to hold the buttons and space them evenly
button_frame = tk.Frame(window)
button_frame.pack(expand=True)

button_width = 20
button_height = 3

# Main variables for the capturing state
is_capturing = False
cancel_commercial_capture = False
cancel_game_capture = False
minimize_after_capture = True



def capture_full_screen(directory):
    """
    Captures a full screenshot using Pillow and saves it with timestamp
    """
    # Create screenshots directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Capture the entire screen
    screenshot = ImageGrab.grab()

    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{directory}/fullscreen_{timestamp}.jpg"

    # Resize to 360p for smaller file size
    screenshot = screenshot.resize((640, 360), ImageGrab.Image.LANCZOS)

    # Save the screenshot
    screenshot.save(filename, "JPEG")
    print(f"Screenshot saved as: {filename}")

def capture_commercial_loop():
    if cancel_commercial_capture:
        return
    if is_capturing:
        capture_full_screen("training_data/commercials")
        window.after(3000, capture_commercial_loop)  # Schedule next capture

def handle_capture_commercial_press():
    try_stop_capture()
    global is_capturing
    is_capturing = True
    global cancel_commercial_capture
    cancel_commercial_capture = False
    capture_commercial_button.config(state="disabled")
    capture_game_button.config(state="disabled")
    capture_commercial_button.config(bg="green")
    if (minimize_after_capture): 
        window.after(1000, window.iconify)  # Minimize after 1 second
    capture_commercial_loop()  # Start the loop

def capture_game_loop():
    if cancel_game_capture:
        return
    if is_capturing:
        capture_full_screen("training_data/game")
        window.after(5000, capture_game_loop)

def handle_capture_game_press():
    try_stop_capture()
    global is_capturing
    is_capturing = True
    global cancel_game_capture
    cancel_game_capture = False
    capture_commercial_button.config(state="disabled")
    capture_game_button.config(state="disabled")
    capture_game_button.config(bg="green")
    if (minimize_after_capture): 
        window.after(1000, window.iconify)  # Minimize after 1 second
    capture_game_loop()

def try_stop_capture():
    global is_capturing
    is_capturing = False
    global cancel_game_capture
    cancel_game_capture = True
    global cancel_commercial_capture
    cancel_commercial_capture = True
    capture_commercial_button.config(state="normal")
    capture_game_button.config(state="normal")
    capture_commercial_button.config(bg="gray")
    capture_game_button.config(bg="gray")

def on_window_deiconify(event):
    try_stop_capture()

window.bind("<Map>", on_window_deiconify)

# Helpers
def toggle_minimize_after_capture():
    global minimize_after_capture
    print("toggling minimize_after_capture" + str(minimize_after_capture))
    minimize_after_capture = not minimize_after_capture

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

minimize_checkbox_status = tk.BooleanVar(value=minimize_after_capture)
minimize_checkbox = tk.Checkbutton(
    window,
    text="Minimize window on capture",
    command=toggle_minimize_after_capture,
    variable=minimize_checkbox_status
).pack()

info_label = tk.Label(
    window,
    text="Window can auto-minimize on capture start; capturing stops when reopened.",
    wraplength=180,
    justify="center"
)
info_label.pack(pady=(15, 5))


window.mainloop()
