import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os
import sys
import json
from datetime import datetime


class IntegratedFlashTool(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MCU Flash Programmer")
        self.geometry("900x700")

        # Configuration State
        self.tool_path = ctk.StringVar(value="")
        self.hex_path = ctk.StringVar(value="")
        self.config_path = ctk.StringVar(value="")
        self.update_json_enabled = ctk.BooleanVar(value=True)

        # --- UI LAYOUT ---
        self.grid_columnconfigure(0, weight=1)

        # 1. Config Section
        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        # Flash Script Path
        ctk.CTkLabel(self.config_frame, text="Flash Script Path"
                                             "py):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.tool_entry = ctk.CTkEntry(self.config_frame, textvariable=self.tool_path, width=400)
        self.tool_entry.grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkButton(self.config_frame, text="Browse Script", command=self.browse_tool).grid(row=0, column=2, padx=10)

        # Firmware File Path
        ctk.CTkLabel(self.config_frame, text="Firmware File (.hex/.srec):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.hex_entry = ctk.CTkEntry(self.config_frame, textvariable=self.hex_path, width=400)
        self.hex_entry.grid(row=1, column=1, padx=10, pady=5)
        ctk.CTkButton(self.config_frame, text="Browse File", command=self.browse_hex).grid(row=1, column=2, padx=10)

        # JSON Config File Path
        ctk.CTkLabel(self.config_frame, text="JSON Config File:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.config_entry = ctk.CTkEntry(self.config_frame, textvariable=self.config_path, width=400)
        self.config_entry.grid(row=2, column=1, padx=10, pady=5)
        ctk.CTkButton(self.config_frame, text="Browse Config", command=self.browse_config).grid(row=2, column=2, padx=10)

        # JSON Update Options
        self.options_frame = ctk.CTkFrame(self.config_frame)
        self.options_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        
        ctk.CTkCheckBox(self.options_frame, text="Update JSON config on successful flash", 
                       variable=self.update_json_enabled).grid(row=0, column=0, padx=10, pady=5)
        
        ctk.CTkButton(self.options_frame, text="View Current JSON", 
                     command=self.view_current_json).grid(row=0, column=1, padx=10, pady=5)

        # 2. Terminal Output
        self.log_area = ctk.CTkTextbox(self, width=860, height=350, font=("Courier New", 12))
        self.log_area.grid(row=1, column=0, padx=20, pady=10)

        # 3. Action Buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, pady=20)
        
        self.flash_btn = ctk.CTkButton(self.button_frame, text="RUN PYTHON FLASH SCRIPT", 
                                      fg_color="#1f538d", hover_color="#14375e",
                                      command=self.start_flash_thread, height=50, width=300)
        self.flash_btn.grid(row=0, column=0, padx=10, pady=10)
        
        self.clear_btn = ctk.CTkButton(self.button_frame, text="Clear Log", 
                                      command=self.clear_log, height=50, width=150)
        self.clear_btn.grid(row=0, column=1, padx=10, pady=10)

    def browse_tool(self):
        path = filedialog.askopenfilename(filetypes=[("Python Script", "*.py")])
        if path: 
            self.tool_path.set(path)
            self.log(f"Selected flash script: {path}")

    def browse_hex(self):
        path = filedialog.askopenfilename(filetypes=[("Firmware Files", "*.hex *.srec *.mot")])
        if path: 
            self.hex_path.set(path)
            self.log(f"Selected firmware file: {path}")

    def browse_config(self):
        path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if path: 
            self.config_path.set(path)
            self.log(f"Selected JSON config file: {path}")

    def log(self, message):
        self.log_area.insert("end", f"{message}\n")
        self.log_area.see("end")

    def clear_log(self):
        self.log_area.delete("1.0", "end")

    def validate_paths(self):
        if not os.path.isfile(self.tool_path.get()):
            messagebox.showerror("Error", "Please select a valid .py flashing script!")
            return False
        if not os.path.isfile(self.hex_path.get()):
            messagebox.showerror("Error", "Firmware file not found!")
            return False
        if self.update_json_enabled.get() and not self.config_path.get():
            messagebox.showerror("Error", "JSON config file path is required when JSON update is enabled!")
            return False
        if self.update_json_enabled.get() and not os.path.isfile(self.config_path.get()):
            messagebox.showerror("Error", "JSON config file not found!")
            return False
        return True

    def update_json_file(self, file_path, new_data):
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

            self.log(f"Successfully updated JSON: {file_path}")
            return True

        except Exception as e:
            self.log(f"Error updating JSON: {e}")
            return False

    def view_current_json(self):
        if not self.config_path.get() or not os.path.isfile(self.config_path.get()):
            messagebox.showwarning("Warning", "Please select a valid JSON config file first!")
            return
        
        try:
            with open(self.config_path.get(), 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Create a new window to display JSON content
            json_window = ctk.CTkToplevel(self)
            json_window.title("Current JSON Configuration")
            json_window.geometry("600x400")
            
            json_text = ctk.CTkTextbox(json_window, font=("Courier New", 11))
            print(json_text)
            json_text.pack(fill="both", expand=True, padx=10, pady=10)
            json_text.insert("1.0", json.dumps(data, indent=4))
            json_text.configure(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read JSON file: {e}")

    def start_flash_thread(self):
        if self.validate_paths():
            self.flash_btn.configure(state="disabled", text="FLASHING...")
            self.clear_log()
            self.log("=== Starting Flash Operation ===")
            self.log(f"Script: {self.tool_path.get()}")
            self.log(f"Firmware: {self.hex_path.get()}")
            if self.update_json_enabled.get():
                self.log(f"JSON Config: {self.config_path.get()}")
            self.log("=" * 50)
            
            thread = threading.Thread(target=self.run_flashing)
            thread.daemon = True  # Ensures thread closes if app is closed
            thread.start()

    def run_flashing(self):
        # Construct command to run the selected script using the current Python interpreter
        command = [
            sys.executable,
            self.tool_path.get(),
            "-f", self.hex_path.get()
        ]

        try:
            # We use 'u' flag or unbuffered mode if necessary, but 'bufsize=1' usually handles it
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            # Stream output line by line to the UI
            for line in process.stdout:
                self.after(0, self.log, line.strip())

            process.wait()

            if process.returncode == 0:
                self.after(0, self.log, "=== Flash Operation Completed Successfully ===")
                
                # Update JSON if enabled
                if self.update_json_enabled.get():
                    self.after(0, self.update_json_after_flash)
                else:
                    self.after(0, lambda: messagebox.showinfo("Success", "Script Executed Successfully!"))
            else:
                self.after(0, self.log, f"=== Flash Operation Failed (Exit Code: {process.returncode}) ===")
                self.after(0,
                           lambda: messagebox.showerror("Error", f"Script failed with exit code {process.returncode}"))

        except Exception as e:
            self.after(0, self.log, f"SYSTEM ERROR: {str(e)}")

        finally:
            self.after(0, lambda: self.flash_btn.configure(state="normal", text="RUN PYTHON FLASH SCRIPT"))

    def update_json_after_flash(self):
        """Update JSON configuration after successful flash operation"""
        # Read existing JSON to preserve current LXSProgrammer path
        try:
            with open(self.config_path.get(), 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except:
            existing_data = {}
        
        custom_input = {
            "flash_script_path": self.tool_path.get(),
            "firmware_file_path": self.hex_path.get(),
            "last_flashed_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "flash_status": "success",
            "python_interpreter": sys.executable
        }
        
        # Preserve existing LXSProgrammer path if it exists
        if "LXSProgrammer_exe_path_dict" in existing_data:
            custom_input["LXSProgrammer_exe_path_dict"] = existing_data["LXSProgrammer_exe_path_dict"]
        
        if self.update_json_file(self.config_path.get(), custom_input):
            messagebox.showinfo("Success", "Flash operation completed successfully and JSON configuration updated!")
        else:
            messagebox.showwarning("Partial Success", "Flash operation completed but JSON update failed. Check log for details.")


if __name__ == "__main__":
    # Set appearance to dark mode for a professional look
    ctk.set_appearance_mode("dark")
    app = IntegratedFlashTool()
    app.mainloop()
