
import tkinter as tk
from tkinter import messagebox

def show_temp_message(message,ms):
    root = tk.Tk()
    root.withdraw()
    #set window size
    w = 400
    h = 300
    #get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    #calculate x and y coordinates  to centre the window
    x = (screen_width // 2) - (w // 2)
    y = (screen_height // 2) - (h // 2)
    msg_win = tk.Toplevel(root)
    msg_win.title("Info")
    #set geometry of window
    msg_win.geometry(f"{w}x{h}+{x}+{y}")
    label = tk.Label(msg_win, text=message, font=("Arial", 12))
    label.pack(expand=True)
    msg_win.attributes("-topmost", True)

    # Destroy window after 5 seconds
    msg_win.after(ms, msg_win.destroy)

    # Wait until window is destroyed
    root.wait_window(msg_win)
    root.destroy()


# #####show info
# def show_temp_message(message):
#     root = tk.Tk()
#     root.withdraw()  # Hide the root window
#
#     msg_win = tk.Toplevel(root)
#     msg_win.title("Info")
#     msg_win.resizable(False, False)
#
#     # Set window size
#     width, height = 300, 100
#
#     # Get screen width and height
#     screen_width = msg_win.winfo_screenwidth()
#     screen_height = msg_win.winfo_screenheight()
#
#     # Calculate position x, y to center the window
#     x = (screen_width // 2) - (width // 2)
#     y = (screen_height // 2) - (height // 2)
#
#     # Set geometry of window
#     msg_win.geometry(f"{width}x{height}+{x}+{y}")
#
#     label = tk.Label(msg_win, text= message, font=("Arial", 12))
#     label.pack(expand=True)
#
#     # Keep window on top
#     msg_win.attributes("-topmost", True)
#
#     # Destroy window after 5 seconds (5000 ms)
#     msg_win.after(5000, msg_win.destroy)
#
#     root.mainloop()
#
# show_temp_message("Please connect Onboard writer to comport")
#