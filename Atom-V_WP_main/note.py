import time
from pywinauto import Application, Desktop

# 1. Start Notepad
# We use wait_for_idle=False to bypass the common launcher warning
Application(backend='uia').start('notepad.exe', wait_for_idle=False)
time.sleep(2)  # Give the UI time to appear

# 2. Use Desktop to find the window
# Fix for ElementAmbiguousError:
# - visible_only=True: Ignores background/hidden processes causing the '7 elements' error
# - found_index=0: Picks the first matching window if multiple are still found
main_window = Desktop(backend='uia').window( title_re=".*Notepad.*",visible_only=True,found_index=0)

main_window.print_control_identifiers()
# 3. Interact with the window
main_window.set_focus()
main_window.type_keys("Automation successful in 2026.\nThis fixed the Ambiguous Error.", with_spaces=True)

# 4. Optional: Print the exact window name found
print(f"Connected to: {main_window.window_text()}")

