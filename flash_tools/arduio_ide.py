import subprocess
from  show_info_popup import show_temp_message
from serial.tools import list_ports
import json

with open('JSON\Arduino_json.json') as filepath:
    json_config = json.load(filepath)
arduino_cli_path = json_config['Arduino_CLI_Path']
arduino_flash_file = json_config['Binary_path']
ARDUINO_CLI = arduino_cli_path
ports = list_ports.comports()

def find_nano_port():
    for port in ports:
        if  "usb" in port.description.lower():
            return port.device
    return None

def flash_arduino(sketch_path):
    # print(ports)
    port = find_nano_port()
    if not port:
        print("Arduino Nano not found!")
        return

    fqbn = "arduino:avr:nano:cpu=atmega328old"  # Old bootloader
    print(f" Found Arduino on {port}")
    print(" Using FQBN:", fqbn)

    try:
        print(" Compiling...")

        subprocess.run([ARDUINO_CLI, "compile", "--fqbn", fqbn, sketch_path], check=True)

        print(" Uploading...")
        subprocess.run([ARDUINO_CLI, "upload", "-p", port, "--fqbn", fqbn,"--verbose", sketch_path], check=True)

        print(" Upload successful!")
        show_temp_message("Dryer arduino code flash successful",10000)
    except subprocess.CalledProcessError as e:
        print(" Flash failed:", e)

# Example sketch path (change this to your actual sketch folder)
flash_arduino(arduino_flash_file)

