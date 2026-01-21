import tkinter as tk
import tkinter.messagebox as msgb
from tkinter.messagebox import showinfo
import pyautogui

def usb_reconnect_fail():
    showinfo(
        title='Failed',
        message=f' Please remove and connect USB ONBOARD WRITER  \n Close application and try again!!!',
        icon='info')

def usb_notconnect_fail():
    showinfo(
        title='Failed',
        message=f' Please Connect USB ONBOARD WRITER  \n Close application and try again!!!',
        icon='info')

def flash_success():
    showinfo(
        title='Success',
        message=f' Flashing Success !!!',
        icon='info')

def flash_failed():
    showinfo(
        title='Fail',
        message=f' Flashing Failed !!!',
        icon='warning')


def show_timed_popup(title, message, timeout_ms):
    """
    Displays a pop-up message that automatically closes after a timeout.

    :param title: The title of the pop-up window.
    :param message: The message to display.
    :param timeout_ms: The duration in milliseconds before the pop-up closes.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main root window

    # Schedule the window to be destroyed after the timeout
    root.after(timeout_ms, root.destroy)

    # Display the message box
    # The 'master=root' argument links it to the hidden root, ensuring proper closure
    msgb.showinfo(title, message, master=root)

    # Start the Tkinter event loop, which will run until root.destroy() is called
    root.mainloop()

