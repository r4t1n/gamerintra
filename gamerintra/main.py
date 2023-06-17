import subprocess
import os
from os.path import expanduser
from pathlib import Path
import shutil

script_location = os.path.dirname(os.path.abspath(__file__))

location = Path(expanduser("~")) / ".config" / "gamerintra"
calendar_location = location / "calendar"
log_location = location / "logs"

conf = location / "gamerintra.conf"

subprocess.run(["mkdir", "-p", calendar_location, log_location])

if not os.path.exists(conf):
    conf_source = os.path.join(script_location, "../gamerintra.conf")
    shutil.copy(conf_source, conf)

subprocess.run(["python", os.path.join(script_location, "getfeed.py")])