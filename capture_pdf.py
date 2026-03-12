import pyautogui
import mss
import time
import os

# Configuration
output_dir = "screenshots"
total_pages = 152
render_delay = 0.5

# Create the screenshots directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Please bring your PDF reader to the foreground.")
print("Starting capture in 5 seconds...")
time.sleep(5)

# Use mss for screenshotting
with mss.mss() as sct:
    for page in range(1, total_pages + 1):
        file_path = os.path.join(output_dir, f"{page}.png")
        
        # Capture the primary monitor and save directly
        sct.shot(output=file_path)
        
        # Press the right arrow key to go to the next page
        pyautogui.press('right')
        
        # Wait for the new page to render
        time.sleep(render_delay)

print("Capture complete.")