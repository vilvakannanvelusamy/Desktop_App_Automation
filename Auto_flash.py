import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os
import sys  # Required to find the current Python interpreter 
import path_locate


class FlashToolApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MCU Python Flash Wrapper v2026")
        self.geometry("800x600")

        # Configuration State
        self.tool_path = ctk.StringVar(value="")
        self.hex_path = ctk.StringVar(value="")

        # --- UI LAYOUT ---
        self.grid_columnconfigure(0, weight=1)

        # 1. Config Section
        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        ctk.CTkLabel(self.config_frame, text="Flash Script Path (.py):").grid(row=0, column=0, padx=10, pady=5)
        self.tool_entry = ctk.CTkEntry(self.config_frame, textvariable=self.tool_path, width=400)
        self.tool_entry.grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkButton(self.config_frame, text="Browse Script", command=self.browse_tool).grid(row=0, column=2, padx=10)

        # 2. File Selection Section
        ctk.CTkLabel(self.config_frame, text="Firmware File (.hex/.srec):").grid(row=1, column=0, padx=10, pady=5)
        self.hex_entry = ctk.CTkEntry(self.config_frame, textvariable=self.hex_path, width=400)
        self.hex_entry.grid(row=1, column=1, padx=10, pady=5)
        ctk.CTkButton(self.config_frame, text="Browse File", command=self.browse_hex).grid(row=1, column=2, padx=10)

        # 3. Terminal Output
        self.log_area = ctk.CTkTextbox(self, width=760, height=300, font=("Courier New", 12))
        self.log_area.grid(row=1, column=0, padx=20, pady=10)

        # 4. Action Button
        self.flash_btn = ctk.CTkButton(self, text="RUN PYTHON FLASH SCRIPT", fg_color="#1f538d", hover_color="#14375e",
                                       command=self.start_flash_thread, height=50)
        self.flash_btn.grid(row=2, column=0, pady=20)

    def browse_tool(self):
        # Updated to filter for Python scripts instead of executables
        path = filedialog.askopenfilename(filetypes=[("Python Script", "*.py")])
        if path: self.tool_path.set(path)

    def browse_hex(self):
        path = filedialog.askopenfilename(filetypes=[("Firmware Files", "*.hex *.srec *.mot")])
        if path: self.hex_path.set(path)

    def log(self, message):
        self.log_area.insert("end", f"{message}\n")
        self.log_area.see("end")

    def validate_paths(self):

        if not os.path.isfile(self.tool_path.get()):
            messagebox.showerror("Error", "Please select a valid .py flashing script!")
            return False
        if not os.path.isfile(self.hex_path.get()):
            messagebox.showerror("Error", "Firmware file not found!")
            return False
        return True

    def start_flash_thread(self):
        if self.validate_paths():
            self.flash_btn.configure(state="disabled", text="FLASHING...")
            self.log_area.delete("1.0", "end")
            thread = threading.Thread(target=self.run_flashing)
            thread.daemon = True  # Ensures thread closes if app is closed
            thread.start()

    def run_flashing(self):
        # Construct command to run the selected script using the current Python interpreter
        # command = [python_exe, your_script.py, arguments...]
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
                self.after(0, lambda: messagebox.showinfo("Success", "Script Executed Successfully!"))
            else:
                self.after(0,
                           lambda: messagebox.showerror("Error", f"Script failed with exit code {process.returncode}"))

        except Exception as e:
            self.after(0, self.log, f"SYSTEM ERROR: {str(e)}")

        finally:
            self.after(0, lambda: self.flash_btn.configure(state="normal", text="RUN PYTHON FLASH SCRIPT"))


if __name__ == "__main__":
    # Set appearance to dark mode for a professional look
    ctk.set_appearance_mode("dark")
    app = FlashToolApp()
    app.mainloop()
