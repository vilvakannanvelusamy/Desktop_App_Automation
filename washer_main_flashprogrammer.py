import os
import configparser
from pywinauto.application import Application
import time
import pytesseract
import pyautogui
import cv2
import numpy as np
import json
import tkinter as tk
from tkinter import messagebox
from  show_info_popup import show_temp_message




# Set your screenshot folder here:
screenshot_folder = r"C:\Users\sachin.r\PycharmProjects\Pythontesting\images\execution_images\Screenshots"

# Minimize all the windows by Simulate pressing the Windows key and D key
pyautogui.hotkey('win', 'd')

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# PyAutoGUI settings
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True


# --- Load configuration from config.ini (if still needed) ---
# config = configparser.ConfigParser()
# config.read("config.ini")
# Example of how to get values if you still use config.ini
# folder_path_from_ini = config.get("FLASHER", "hex_folder", fallback=r"D:\path_to\Ver2")
# com_keyword = config.get("FLASHER", "com_port_keyword", fallback="COM")

# --- Load configuration from config.json ---
try:
    with open('Flash_programmer_json.json', 'r') as f:
        json_config = json.load(f)
    flash_programmer_path = json_config['flash_programmer_path_dict']
    # Renaming for clarity as per the config.json structure
    hex_folder_path = json_config['dryer_main_binary_path']
    model_name = json_config['model_name_dict']
    # REMOVED: display_binary_path = json_config['binary_paths']['display_binary_path']
    print(f"Loaded Flash Programmer Path: {flash_programmer_path}")
    print(f"Loaded HEX Folder Path: {hex_folder_path}")
except FileNotFoundError:
    print("Error: config.json not found. Please create it with the necessary paths.")
    exit() # Exit if the config file is crucial
except KeyError as e:
    print(f"Error: Missing key in config.json: {e}. Please check your config.json structure.")
    exit()


# OCR Click Helper
def click_on_text(target_text):
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    # Debug: Print all detected non-empty texts
    # print("Detected texts on screen:")
    # print([text for text in data['text'] if text.strip() != ""])

    for i, text in enumerate(data['text']):
        if target_text.lower() in text.lower():
            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]
            center_x = x + w // 2
            center_y = y + h // 2
            print(f"Clicking '{text}' at ({center_x}, {center_y})")
            pyautogui.moveTo(center_x, center_y)
            time.sleep(0.5)
            pyautogui.click()
            return True
    print(f"'{target_text}' not found on screen.")
    return False


# Step 1: Launch the FLASH Programmer
# Use the path loaded from config.json
app = Application(backend='uia').start(flash_programmer_path)
main_window = app.window(title_re=".*FLASH Programmer.*")
main_window.wait('visible', timeout=20)
#main_window.set_focus(\\10.221.90.126\joy.graceson\yathendra\FX_Models Virtualization\FX 25kg Auto DT KR\Ver1\Main_PJT_470_F33D.hex)
main_window.restore()
time.sleep(2)

# Step 2: Click OK
try:
    main_window.child_window(title="OK", control_type="Button").click_input()
    print("Clicked OK")
except Exception as e:
    print("OK button error:", e)
time.sleep(1)

# Step 3: Click Cancel
try:
    cancel_button = app.window(title_re=".*").child_window(title_re="(?i)Cancel", control_type="Button")
    cancel_button.wait('enabled', timeout=10)
    cancel_button.click_input()
    print("Clicked Cancel button")
except Exception as e:
    print("Cancel button not found:", e)
time.sleep(2)

# Step 4: Use OCR to click 'File' menu
click_on_text("File")
time.sleep(2)

# Step 5: Use OCR to click 'Open Object File...'
click_on_text("Open")

# Delete the entry box
time.sleep(1)
pyautogui.press("backspace")

# Enter the Driver code path
time.sleep(1)
# Step 7: Automatically detect the .hex file in the folder
# Use the path loaded from config.json
folder_path_for_hex = hex_folder_path
print(f"Checking folder path for HEX files: {folder_path_for_hex}")

# Check if the folder exists
if os.path.exists(folder_path_for_hex) and os.path.isdir(folder_path_for_hex):
   try:
       hex_files = [f for f in os.listdir(folder_path_for_hex) if f.lower().endswith('.hex')]
       if hex_files:
           hex_filename = hex_files[0]
           hex_full_path = os.path.join(folder_path_for_hex, hex_filename)
           print(f"Auto-selected HEX file: {hex_full_path}")
           pyautogui.typewrite(hex_full_path)
           pyautogui.click() # Clicking after typing can sometimes help with focus
           time.sleep(2)
           # pyautogui.press("enter") # Removed as pyautogui.click() might be enough or cause issues after typewrite
       else:
           print("No .hex files found in the folder!")
   except Exception as e:
       print(f"Error reading the folder: {e}")
else:
   print(f"Error: The folder path '{folder_path_for_hex}' does not exist or is invalid.")
time.sleep(2)
pyautogui.press("enter") # Press enter to confirm the file selection
main_window.close()
print("Closed Flash Programmer after loading HEX")


# #####show info
show_temp_message("Please connect Onboard writer to comport",5000)
# show_temp_message()

time.sleep(10)
# Relaunch tool
# Use the path loaded from config.json
app = Application(backend='uia').start(flash_programmer_path)
main_window = app.window(title_re=".*FLASH Programmer.*")
main_window.wait('visible', timeout=20)
main_window.set_focus()
main_window.restore()
time.sleep(2)

try:
   main_window.child_window(title="OK", control_type="Button").click_input()
   print("Clicked OK")
except: print("OK not found")
time.sleep(2)

try:
    cancel_button = app.window(title_re=".*").child_window(title_re="(?i)Cancel", control_type="Button")
    cancel_button.wait('enabled', timeout=10)
    cancel_button.click_input()
    print("Clicked Cancel button")
except Exception as e:
    print("Cancel button not found:", e)

# Setup -> Communication
try:
    setup_button = app.window(title_re=".*").child_window(title_re="(?i)Setup", control_type="Button")
    setup_button.wait('enabled', timeout=10)
    setup_button.click_input()
    print("Clicked Setup button")
except Exception as e:
    print("Setup button not found:", e)
time.sleep(2)

# Step 5: Use OCR to click 'Open Object File...' (This comment is wrong, should be "Communication")
click_on_text("Communication")

time.sleep(1)

# Assuming this OK is for the Communication settings dialog
try:
   main_window.child_window(title="OK", control_type="Button").click_input()
   print("Clicked OK on Communication settings.")
except: print("OK button on Communication settings not found.")
time.sleep(2)

try:
    pyautogui.hotkey('ctrl','a')

except Exception as e:
    print("pyautogui not work")

from pywinauto import Application, Desktop

try:
   # This 'Start' button is likely on the "Auto Programming" window that appears.
   # You might need to target that specific window instead of main_window's child_window
   # If 'main_window' is still the main Flash Programmer window, this might click the wrong 'Start'.
   # Let's try to find the "Auto Programming" window first, if it's a separate dialog.
   auto_programming_window = Desktop(backend="uia").window(title_re="Auto Programming")
   if auto_programming_window.exists(timeout=1):
        auto_programming_window.child_window(title="Start", control_type="Button").click_input()
        print("Clicked Start button on Auto Programming window.")
   else:
       # Fallback to main_window if it's not a separate dialog
       main_window.child_window(title="Start", control_type="Button").click_input()
       print("Clicked Start button (fallback to main window).")

except Exception as e:
    print(f"Start button not found or error clicking it: {e}")

time.sleep(2)
try:
    # Connect to the app - modify as needed
    app = Application(backend="uia").connect(title_re="FLASH Programmer")
    # Access the dialog window
    popup = app.window(title_re="FLASH Programmer")


    if popup.exists():
        try:
        # Access the 'OK' button inside the dialog
            ok_btn = popup.child_window(title="OK", auto_id="2", control_type="Button")
        # Click the 'OK' button to close the popup
            ok_btn.click_input()
        except Exception as e:
            print("could not close")
        try:
            cancel_button = popup.child_window(title="Cancel", auto_id="2", control_type="Button")
            cancel_button.click_input()
        except Exception as e:
            print("cancel button not available")
    time.sleep(2)

    app = Application(backend="uia").connect(title_re="FLASH Programmer")

    # Get main window
    main_win = app.window(title_re="FLASH Programmer")

# Open Setup menu
# Select Password... menu item (using exact path or direct child window)
    main_win.menu_select("Setup->Password...")

# Alternatively, if menu_select doesn't work, try clicking the MenuItem control directly
# password_item = main_win.child_window(title="Password...", control_type="MenuItem")
# password_item.click_input()
#password entry
    time.sleep(2)
    app = Application(backend="uia").connect(title_re="FLASH Programmer")

# Get main window
    setup_pass_win = app.window(title_re="FLASH Programmer")
# setup_pass_win.child_window(title="Setup Password", control_type="Window")

    manual_radio_button = setup_pass_win.child_window(title="Manual", auto_id="1191", control_type="RadioButton")
    device_in_blank_radio_button = setup_pass_win.child_window(title="Device is Blank", auto_id="1188", control_type="RadioButton")

    if manual_radio_button.is_selected():
        device_in_blank_radio_button.click_input()
        print(manual_radio_button.window_text())
    elif device_in_blank_radio_button.is_selected():
    # device_in_blank_radio_button.click_input()
        manual_radio_button.click_input()
        setup_pass_win.child_window(title="Password", auto_id="1104", control_type="Edit").click_input()
        pyautogui.write('0102030405060708090a0b0c')
        print(device_in_blank_radio_button.window_text())

    time.sleep(2)
    setup_pass_win.child_window(title="OK", auto_id="1", control_type="Button").click_input()
    time.sleep(2)
    main_window.close()
    show_temp_message(model_name + "\n Password handled  \n Please rerun again!!!", 10000)
    print(main_window.print_control_identifiers())

except Exception as e:
    print("Could not handle password")





#
# Create screenshot folder path relative to script location
screenshot_folder = os.path.join(os.getcwd(), "images", "execution_images", "screenshots")
os.makedirs(screenshot_folder, exist_ok=True)

# Use timestamp to generate unique screenshot file
timestamp = time.strftime("%Y%m%d_%H%M%S")
screenshot_path = os.path.join(screenshot_folder, f"flash_result_{timestamp}.png") # Changed filename

# Save the screenshot of the main window or current active window
try:
    Desktop(backend='uia').top_window().capture_as_image().save(screenshot_path)
    print(f"Screenshot saved at: {screenshot_path}")
except Exception as e:
    print(f"Failed to capture screenshot: {e}")

# # After success
#    log_message("Washer main flashing failed.")
completed = False
max_tries = 120
retry_count = 0
while not completed  and retry_count < max_tries:
    try:
        txt = main_window.child_window(title="OK", auto_id="1185", control_type="Text").window_text()
        print(txt)
        if txt == "OK" :
            completed = True
            show_temp_message(model_name + " \nflash success",10000)
    except Exception as e:
        pass

    retry_count +=1
    time.sleep(1)
if not completed:
        show_temp_message(model_name +  " \nFlash Failed",10000)
time.sleep(1)
main_window.child_window(title="No", auto_id="2", control_type="Button").click_input()
time.sleep(1)
main_window.child_window(title="Cancel", auto_id="2", control_type="Button").click_input()
time.sleep(1)
main_window.close()
# print(main_window.print_control_identifiers())
