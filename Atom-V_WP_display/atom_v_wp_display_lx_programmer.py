import time
import pyautogui
from pywinauto import Application, ElementNotFoundError
from tkinter.messagebox import showinfo
import json
import argparse
import sys


# Minimize all the windows by Simulate pressing the Windows key and D key
pyautogui.hotkey('win','d')

import os

# Get the directory where the script itself is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, 'json', 'config_json.json')

def update_config_firmware_path(new_firmware_path):
    """Update the firmware_file_path in the JSON config file"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        config_data['firmware_file_path'] = new_firmware_path
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)
        
        print(f"Updated firmware path in config: {new_firmware_path}")
        return True
    except Exception as e:
        print(f"Error updating config: {e}")
        return False

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='MCU Flash Tool with Dynamic Config Update')
    parser.add_argument('-f', '--firmware', type=str, 
                       help='Path to firmware file (.hex/.srec)')
    return parser.parse_args()

# Parse command line arguments
args = parse_arguments()

# Update config if firmware path provided via command line
if args.firmware:
    if not update_config_firmware_path(args.firmware):
        print("Failed to update config file. Exiting.")
        sys.exit(1)

print(config_path)

with open(config_path) as json_file:
    config_json_data = json.load(json_file)


#
# with open('json\config_json.json') as json_file:
#     config_json_data = json.load(json_file)


LXSProgrammer_exe_path_r = r"{}".format(config_json_data["LXSProgrammer_exe_path_dict"])
# display_binary_path = r'D:\FOTA FWs\DIsplay_Sub\ATOM-V_WaterPurifier_Display\SW31100_for_LG_REF_Atom_V_SAA43766201_0xFB67.hex'
display_binary_path = r"{}".format(config_json_data["firmware_file_path"])
print(display_binary_path)


# print("LXSProgrammer_exe_path_r=r'D:/Kitchen/flash_tool/Atom_V/LXSProgrammer_Atom-V_Disp/LXSProgrammer.exe'")
# print("display_binary_path=r'D:\FOTA FWs\DIsplay_Sub\ATOM-V_WaterPurifier_Display\SW31100_for_LG_REF_Atom_V_SAA43766201_0xFB67.hex'",display_binary_path)



# launch LXSProgrammer.exe
try:
    app = Application(backend='uia').start(LXSProgrammer_exe_path_r)
    lx_programmer_window = app.window()
    time.sleep(1)
    print("Application window opened")

except ElementNotFoundError as e:
    print("Application not found")

# lx_programmer_window.print_control_identifiers()

# Locate and click on browse button
try:
    browse_button = lx_programmer_window.child_window(title="Browse", auto_id="buttonBrowse", control_type="Button")
    browse_button.click_input()
    time.sleep(1)
    print("Browse button clicked")

except ElementNotFoundError as e:
    print("Browse Button not found")

#control sub window
browse_file = app.window()

# click on file name edit box
try:
    click_on_file_name_edit = browse_file.child_window(title="File name:", auto_id="1148", control_type="Edit")
    click_on_file_name_edit.click_input()
    print("File name edit clicked")

except ElementNotFoundError as e:
    print("File name element not found")

# enter hex file path
pyautogui.write(display_binary_path)
time.sleep(1)
pyautogui.press('enter')
print(".hex file path added successfully")

# Locate and click on connect button
try:
    click_connect_button = browse_file.child_window(title="Connect", auto_id="buttonConnect", control_type="Button")
    click_connect_button.click()
    time.sleep(3)
    print("Connect button clicked")
except ElementNotFoundError as e:
    print("Connect button not found")

# Locate and click on Execute button
try:
    time.sleep(5)
    click_on_execute_button = browse_file.child_window(title="Execute", auto_id="buttonExecute", control_type="Button")
    print(click_on_execute_button.window_text())
    if click_on_execute_button.is_enabled():
        print("Execute button is enabled")
        click_on_execute_button.click()  # Click the button if enabled

    else:
        print("Execute button is disabled")
        showinfo(
            title='Failed',
            message=f' USB ONBOARD WRITER NOT CONNECTED \n Close application and try again!!!',
            icon='info')
except ElementNotFoundError as e:

    print("Execute button not found")

time.sleep(5)

# browse_file.print_control_identifiers()

# analyse result pass/fail

result = browse_file.child_window( auto_id="labelProgramStatus", control_type="Text")

checksum = browse_file.child_window( auto_id="labelChecksum", control_type="Text")

print(f'flashing status is {result.window_text()}')
print(f'checksum is {checksum.window_text()}')

try:

    if result.window_text() == 'OK':
        print("Flashing Success")
        showinfo(
            title='Success',
            message= f'{checksum.window_text()}  Flashing Success !!!',
            icon='info')
    else:
        print("Flashing Failed")
        showinfo(
            title='Fail',
            message=f'{checksum.window_text()}  Flashing Failed !!!',
            icon='warning')
except ElementNotFoundError as e:
    print("Result cannot be found")

browse_file.close()



