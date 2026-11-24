import subprocess
import json
from pathlib import Path

result = subprocess.run([r"tools\flpdiff.exe", "info",
 r"C:\BeatTest\weesd91926.flp", "--format", "json"],
  capture_output=True, text=True, timeout=60)
print(result.stderr)
print(result.returncode)

data = json.loads(result.stdout)

for channel in data["channels"]:
    if channel["plugin"] is not None:
        print(channel["name"], channel["plugin"]["name"])
    else:
        print(channel["name"], Path(channel["sample_path"]["value"]).parent.parent.name)