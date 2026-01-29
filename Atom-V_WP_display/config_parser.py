import os
import json
import argparse
import sys



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, 'json', 'config_json.json')

def update_config_firmware_path(new_firmware_path):
    """Update the firmware_file_path in the JSON config file"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)

        # Convert forward slashes to backward slashes for Windows compatibility
        normalized_path = new_firmware_path.replace('/', '\\')
        config_data['firmware_file_path'] = normalized_path

        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)

        print(f"Updated firmware path in config: {normalized_path}")
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

