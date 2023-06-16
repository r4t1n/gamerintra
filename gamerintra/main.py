import subprocess
import sys
import os
from os.path import expanduser
import shutil
import time

location = expanduser("~") + "/.config/gamerintra/"
calendar_location = location + "calendar/"
log_location = location + "logs/"

conf = os.path.join(location, "gamerintra.conf")
feed = os.path.join(calendar_location, "GetFeed.ics")
feed_new = os.path.join(calendar_location, "GetFeed_new.ics")

current_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
wget_log = log_location + "wget_log_" + current_time

# We can run the mkdir command even if the directories are made since it does not override files and does not print to the terminal
subprocess.run(["mkdir", "-p", calendar_location, log_location])

# If the config file does not exist we copy the default config file, prompt the user to enter their URL and then write the URL to the config file
if not os.path.exists(conf):
    shutil.copy("../gamerintra.conf", location)
    url = input("Enter full URL from SkoleIntra: ")

    with open(conf, 'r') as file:
        lines = file.readlines()
    
    updated_lines = []
    for line in lines:
        if line.startswith("url = "):
            line = f"url = {url}\n"
        updated_lines.append(line)
    
    with open(conf, 'w') as file:
        file.writelines(updated_lines)

# If the config file does exist we read from the file and store the url in the url variable (maybe use open again instead of using cat and grep for this)
url_output = subprocess.check_output("cat {} | grep 'url = '".format(conf), shell=True).decode(sys.stdout.encoding).strip()
url = url_output.replace("url = ", "")

subprocess.run(["wget", "-o", wget_log, "-O", feed_new, url])

# "--ignore-matching-lines=^DTSTAMP:................" is needed to ignore the timestamp of downloading since this changes every time you download the file
# "stdout=subprocess.DEVNULL" and "stderr=subprocess.DEVNULL" is used to supress diff outputting to the terminal
diff_process = subprocess.run(
    ["diff", "-q", "--ignore-matching-lines=^DTSTAMP:................", feed_new, feed],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# Return code 0 = The files are identical
# Return code 1 = The files are not identical
# Return code 2 = No such file or directory
if diff_process.returncode == 0:
    os.remove(feed_new)
elif diff_process.returncode == 1 or diff_process.returncode == 2:
    shutil.move(feed_new, feed)