import time
import pyautogui
from pywinauto import Application, ElementNotFoundError,keyboard
import popup
import json
import config_parser as cp
config_path = cp.config_path

pyautogui.hotkey('win','d')
time.sleep(1)


with open(config_path) as json_file:
    config_json_data = json.load(json_file)


renesas_exe_path_r = r"{}".format(config_json_data["renesas_exe_path_dict"])
driver_code_path = r"{}".format(config_json_data["driver_code_path_dict"])
display_binary_path = r"{}".format(config_json_data["firmware_file_path"])
# drier_code_var = config_json_data["drier_code_var_dict"]

# app = Application(backend='uia').start(r"C:\Program Files (x86)\Renesas Electronics\Programming Tools\Renesas Flash Programmer V3.17\RFPV3.exe")

app = Application(backend='uia').start(renesas_exe_path_r)
time.sleep(1)
main_window = app.window(title_re="Renesas Flash Programmer V3.17.00")
title = main_window.window_text()
print(title)
if title == "Renesas Flash Programmer V3.17.00":
    print(f"{title} is opened")
else:
    print(f"{title} is not opened")

# main_window.print_control_identifiers()

# select open project on file menu
pyautogui.hotkey('alt', 'f')
pyautogui.press('down')
pyautogui.press('enter')

# main_window.print_control_identifiers()
# Locate and click_on_file_name_edit
try:
    click_on_file_name_edit = main_window.child_window(title="File name:", auto_id="1148", control_type="Edit")
    click_on_file_name_edit.click_input()
    print("File name is clicked")

except ElementNotFoundError as e:
    print("File name is not clicked")

# enter .hex file path

pyautogui.hotkey('ctrl', 'a')
pyautogui.press('delete')
pyautogui.write(driver_code_path)
pyautogui.press('enter')

# click on Add/Remove file button
try :
    click_on_Add_Remove_file_button = main_window.child_window(title="Add/Remove Files...", auto_id="buttonFileDetails", control_type="Button")
    click_on_Add_Remove_file_button.click_input()
    print("Add/Remove Files clicked")

except ElementNotFoundError as e:
    print("Add/Remove Files is not clicked")

# main_window.print_control_identifiers()
#  Select existing hex file
try :
    select_exixting_file = main_window.child_window(title="File Name Row 0", control_type="DataItem")
    select_exixting_file.click_input()
    print(" selected Existing file ")

except ElementNotFoundError as e:
    print("Selected File is not clicked")

# click on remove file button
try:
    click_on_Remove_file = main_window.child_window(title="Remove Selected File(s)\r\n", auto_id="buttonRemove", control_type="Button")
    click_on_Remove_file.click_input()
    print("Remove Selected Files Button clicked")

except ElementNotFoundError as e:
    print("Remove Selected Files Button is not clicked")

# click on Add files button

try:
    click_on_Add_file_button = main_window.child_window(title="Add File(s)...", auto_id="buttonAdd", control_type="Button")
    click_on_Add_file_button.click_input()
    print("Add Files Button clicked")

except ElementNotFoundError as e:
    print("Add Files is not clicked")

# cilck on file name when add .hex file
try:
    click_on_hex_file_name_edit = main_window.child_window(title="File name:", auto_id="1148", control_type="Edit")
    click_on_hex_file_name_edit.click_input()
    print(".hex File name edit is clicked")

except ElementNotFoundError as e:
    print(".hex File name edit is not clicked")

pyautogui.write(display_binary_path)
pyautogui.press('enter')

# click on ok button after .hex file selection
try:
    click_on_ok_after_hexfile_selection = main_window.child_window(title="OK", auto_id="buttonOK", control_type="Button")
    click_on_ok_after_hexfile_selection.click_input()
    print("OK button after hexfile selection clicked")


except ElementNotFoundError as e:
    print("OK button after hexfile selection is not clicked")

# click on connect setting button
try:
    click_on_connect_setting_button = main_window.child_window(title="Connect Settings", control_type="TabItem")
    click_on_connect_setting_button.click_input()
    print("Connect Settings button clicked")


except ElementNotFoundError as e:
    print("Connect Settings button is not clicked")

# click on speed dropdown and enter 115200 bps
try:
    click_on_speed_edit_box = main_window.child_window(title="Speed:", auto_id="comboBoxSpeed", control_type="ComboBox")
    click_on_speed_edit_box.click_input()
    print("Speed edit box clicked")
    pyautogui.hotkey('ctl','a')
    pyautogui.write("1,15,200")
    pyautogui.press('enter')

except ElementNotFoundError as e:
    print("Speed edit box is not clicked")

# click on tool details button
try:
    click_on_tool_details_button = main_window.child_window(title="Tool Details...", auto_id="buttonToolDetail", control_type="Button")
    click_on_tool_details_button.click_input()
    print("Tool Details button clicked")

except ElementNotFoundError as e:
    print("Tool Details button is not clicked")
# main_window.print_control_identifiers()
# comport selection
try:
    time.sleep(2)
    # select_tool = main_window.child_window(title="Select Tool", control_type="TabItem")
    # select_tool.click()
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('down')
    time.sleep(1)
    # keyboard.send_keys("{DOWN}")
    # select_comport = main_window.child_window(title = "File Name Row 0", control_type = "ListItem")
    # select_comport = main_window.child_window(title="COM11 : Silicon Labs CP210x USB to UART Bridge",
                                              # auto_id="listBoxTool", control_type="List")
    # select_comport.select()
    print("COMPORT selected")

except ElementNotFoundError as e:
    print("COMPORT not selected")
    popup.usb_notconnect_fail()

# click on ok after comport selection
try:
    click_on_ok_after_comport_select = main_window.child_window(title="OK", auto_id="buttonOK", control_type="Button")
    click_on_ok_after_comport_select.click_input()
    print("OK button after comport selection clicked")

except ElementNotFoundError as e:
    print("OK button after comport selection is not clicked")

# click on operation tab
try:
    click_on_operation_tab = main_window.child_window(title="Operation", control_type="TabItem")
    click_on_operation_tab.click_input()
    print("Operation tab clicked")

except ElementNotFoundError as e:
    print("Operation not selected")

# click on start button
try:
    click_on_start_button = main_window.child_window(title="Start", auto_id="buttonStart", control_type="Button")
    click_on_start_button.click_input()
    print("Start button clicked")

except ElementNotFoundError as e:
    print("Start button not clicked")

time.sleep(5)

#     Authentication part
try:
    authentication_window = main_window.child_window(title="Authentication", auto_id="IDCodeAndPwdDlg", control_type="Window")
    print("Authentication window ")
    if authentication_window.exists():
    #     print("Enter Authentication Code")
        for c in range(3):
            authentication_code_edit = main_window.child_window(title="Authentication Code", auto_id="groupBox",
                                                                control_type="Group")
            authentication_code_edit.click_input()
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            pyautogui.write("4FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
            click_ok_after_authentication = main_window.child_window(title="OK", auto_id="buttonOK",
                                                                     control_type="Button")
            click_ok_after_authentication.click_input()
            time.sleep(2)


        main_window.child_window(title="Cancel", control_type="Button").click()
        popup.show_timed_popup("Alert", "Please remove and reconnect ONBOARD WRITER", "5000")
        time.sleep(10)

        click_on_start_button_2 = main_window.child_window(title="Start", auto_id="buttonStart", control_type="Button")

        click_on_start_button_2.click_input()
        # print("after start click 2nd")

except ElementNotFoundError as e:
    print("Authentication code is not clicked")

time.sleep(50)

# verify result
try:
    result_status_string = main_window.child_window(title="OK", auto_id="labelStatus", control_type="Text")
    print(result_status_string.window_text())
    if result_status_string.window_text() == "OK":
        print("Flashing Success")
        popup.flash_success()
    else:
        print("Flashing Failed")
        popup.flash_failed()


except ElementNotFoundError as e:
    print("Result status is not found")



# main_window.print_control_identifiers()


