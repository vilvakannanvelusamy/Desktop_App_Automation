import json
import os
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Auto_flash import FlashToolApp
# C:\Users\vilvakannan.velusamy\PycharmProjects\PythonProject_flash_tool\Auto_flash.py

def update_json_file(file_path, new_data):
    """
    Reads a JSON file, updates it with custom input (dictionary),
    and writes it back to the file.
    """
    try:
        # Step 1: Load existing data if file exists
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            # Create a new empty dictionary if file doesn't exist
            data = {}

        # Step 2: Update with custom input
        # Use update() to merge or add new key-value pairs
        data.update(new_data)

        # Step 3: Write back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            # indent=4 makes the file human-readable
            json.dump(data, f, indent=4)

        print(f"Successfully updated: {file_path}")
        return True

    except Exception as e:
        print(f"Error updating JSON: {e}")
        return False


# --- Usage Example for your Flashing Tool ---
config_file = r"C:/Users/vilvakannan.velusamy/PycharmProjects/PythonProject_flash_tool/Atom-V_WP_display/json/config_json.json"
# Create FlashToolApp instance to access its variables
app = FlashToolApp()
custom_input = {
    "atom_v_wp_display_bin_path_dict": f"{app.tool_path.get()}",
    "last_flashed_date": "2026-01-16"
}

update_json_file(config_file, custom_input)
