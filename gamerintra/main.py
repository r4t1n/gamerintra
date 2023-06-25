import subprocess
import os
from os.path import expanduser
from pathlib import Path
import shutil
import colorama

colorama.init()

ok = " [" + colorama.Fore.GREEN + "+" + colorama.Style.RESET_ALL + "] "
warning = colorama.Fore.YELLOW + " [" + colorama.Fore.RED + "!" + colorama.Fore.YELLOW + "] " + colorama.Style.RESET_ALL

green = colorama.Fore.GREEN
style_reset = colorama.Style.RESET_ALL

script_location = os.path.dirname(os.path.abspath(__file__))

location = Path(expanduser("~")) / ".config" / "gamerintra"
calendar_location = location / "calendar"
log_location = location / "logs"

conf = location / "gamerintra.conf"

subprocess.run(["mkdir", "-p", calendar_location, log_location])

if not os.path.exists(conf):
    conf_source = os.path.join(script_location, "../", "gamerintra.conf")
    print(warning + "Config file not found, copying " + green + str(conf_source) + style_reset + " to " + green + str(conf) + style_reset)
    shutil.copy(conf_source, conf)

subprocess.run(["python3", os.path.join(script_location, "getfeed.py")])
