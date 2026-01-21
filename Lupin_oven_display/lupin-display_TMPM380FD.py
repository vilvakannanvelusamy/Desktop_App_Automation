import time
import pyautogui
from pywinauto import Application, ElementNotFoundError
import popup
import json


# minimize all window
pyautogui.hotkey('win','d')
time.sleep(1)


with open('json\config_json.json') as json_file:
    config_json_data = json.load(json_file)


tmpm380fd_exe_path_r = r"{}".format(config_json_data["tmpm380fd_exe_path_dict"])
display_binary_path = r"{}".format(config_json_data["lupin_display_bin_path_dict"])


print("tmpm380fd_exe_path_r=",tmpm380fd_exe_path_r)
print("display_binary_path=",display_binary_path)



def handle_initial_dialog(app_path):
    """
    Launches the application at the specified path and attempts to dismiss
    an initial "OK" or "Cancel" dialog box using pywinauto.

    Args:
        app_path (str): The file path to the executable (e.g., r"D:\...exe").
    """
    try:

        global app
        # Start the application using UIA backend
        app = Application(backend='uia').start(app_path)
        time.sleep(2)  # Give the application time to launch and the dialog to appear

        # Get the main window reference
        global main_window_tool
        main_window_tool = app.window()

        print(f"Application launched. Main window title: '{main_window_tool.window_text()}'")

    except Exception as e:
        print(f"An error occurred during application launch or initial interaction: {e}")
        return None  # Return None if launch failed

        # --- Attempt to click "OK" ---
    try:
            ok_button = main_window_tool.child_window(title="OK", control_type="Button")
            ok_button.click()
            print("Successfully clicked 'OK' button.")
             # Return the app object for further automation

    except ElementNotFoundError:
            print("OK button element not found. Trying 'Cancel'...")

    time.sleep(1)
            # --- Attempt to click "Cancel" if "OK" failed ---

    try:
            cancel_button = main_window_tool.child_window(title="Cancel", control_type="Button")
            cancel_button.click()
            print("Successfully clicked 'Cancel' button.")
              # Return the app object for further automation

    except ElementNotFoundError:
                print("Cancel button element not found either. Initial dialog handling complete (no buttons clicked).")
                return app  # Return the app object anyway




# --- Example Usage ---
    # Define the path to your executable
    # Replace with the actual path on your system
# executable_path = r"D:\Kitchen\flash_tool\Lupin_Oven\380_383_Lupin_Disp\bin\FlashProgCM.exe"

    # Call the function
handle_initial_dialog(tmpm380fd_exe_path_r)

# if running_app:
#         print("\nFunction finished. The application is now running and ready for next steps.")
#         # You can continue automation using the returned 'running_app' object
#         # e.g., running_app.window().child_window(title="AnotherControl").click()
#     else:
#         print("\nAutomation stopped due to an error.")



time.sleep(1)
# main_window.print_control_identifiers()
#Click on file menu and  select open object file menu
main_window_tool.menu_select("File-> Open Object File...'")

# click on file name edit box

try:
    click_on_file_name_edit = main_window_tool.child_window(title="File name:", auto_id="1090", control_type="Text")
    click_on_file_name_edit.click_input()
    print("file name edit box clicked")
    pyautogui.hotkey('ctrl','a')
    pyautogui.write(display_binary_path)
    pyautogui.press('enter')

except ElementNotFoundError as e:
     print("File name edit box element not found")

time.sleep(1)
popup.show_timed_popup("Alert", "please connect ONBOARD WRITER  \n within 5 seconds", timeout_ms=3000)

main_window_tool.close()
time.sleep(3)
handle_initial_dialog(tmpm380fd_exe_path_r)
time.sleep(1)

# click on setup menu and select commuincation
try:
    main_window_tool.menu_select("Setup-> Communication...")
    print("commuication setup selected ")


except ElementNotFoundError as e :
    print("setup menu element not found")
time.sleep(1)


# main_window.print_control_identifiers()
# # Com port selection
# try:
#     comport_dropdown = main_window.Static2
#     print(comport_dropdown.windows_text())
#     comport_dropdown.click()
#
# except ElementNotFoundError as e :
#     print("comport selection failed")




# click on ok in setup menu
try:
    click_on_setup_okbutton = main_window_tool.child_window(title="OK", auto_id="1", control_type="Button")
    click_on_setup_okbutton.click_input()
    print("setup ok button clicked")

except ElementNotFoundError as e :
    print(" setup ok button not found")

pyautogui.hotkey('ctrl','shift','q')
time.sleep(1)

#  click on Erase 'E' button

try:
    click_on_erase_button = main_window_tool.child_window(title="ChipErase", control_type="Button")
    click_on_erase_button.click()
    print("ChipErase button clicked")

except ElementNotFoundError as e :
    print("ChipErase button not found")

time.sleep(1)

# click on chip erase ok button

try:
    click_on_chip_erase_ok_button = main_window_tool.child_window(title="OK", auto_id="1", control_type="Button")
    click_on_chip_erase_ok_button.click()
    time.sleep(1)
    pyautogui.press('enter')
    print("ChipErase ok button clicked ")

except ElementNotFoundError as e :
    print("ChipErase ok button not found")

main_window_tool.close()
popup.show_timed_popup("Alert", "please Remove and connect ONBOARD WRITER \n Within 5 seconds ",
                       timeout_ms=3000)
time.sleep(3)
handle_initial_dialog(tmpm380fd_exe_path_r)


#     click on Auto programming button
try:
    click_on_auto_program_button = main_window_tool.Button13
    click_on_auto_program_button.click_input()
    print("Auto program button clicked")

except ElementNotFoundError as e :
    print("Auto program button not found")

time.sleep(60)

# Flash status verification

status = main_window_tool.Static4
checksum = main_window_tool.Static2
if status.window_text() == 'Programming completed successfully.' :
    print(f'{checksum.window_text()} {status.window_text()}')

else :
    print(f'{checksum.checksum.window_text()} {status.window_text()}')

time.sleep(3)

# click on No button after flash
try:
    click_on_okbutton_after_flash = main_window_tool.child_window(title="No", auto_id="2", control_type="Button")
    click_on_okbutton_after_flash.click()

except ElementNotFoundError as e :
    print("ok button not found")

time.sleep(2)
main_window_tool.close()
#
# main_window.print_control_identifiers()
#
# # comport selection
# #  child_window(title="COM Port", auto_id="1040", control_type="Text")
# #
# # throw popup for NO comport   list