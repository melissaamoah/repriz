# Spike 1, Part 2: run FL Studio's command-line export from Python

import subprocess

try:
    subprocess.run([r"C:\Program Files\Image-Line\FL Studio 2024\FL64.exe", 
    "/R", "/Emp3", r"C:\BeatTest\weesd91926.flp"], timeout=60)
    print("FL Studio Finished")
except subprocess.TimeoutExpired:
    print("FL Studio timed out")



