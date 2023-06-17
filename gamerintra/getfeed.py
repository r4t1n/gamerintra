import subprocess
import os
from os.path import expanduser
from pathlib import Path
import shutil
import re
import time


location = Path(expanduser("~")) / ".config" / "gamerintra"
calendar_location = location / "calendar"
log_location = location / "logs"

conf = location / "gamerintra.conf"
feed = calendar_location / "GetFeed.ics"
feed_new = calendar_location / "GetFeed_new.ics"

current_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
wget_log = str(log_location) + "/wget_log_" + current_time

skoleintra_url_pattern = r"https://.*?\.m\.skoleintra\.dk/feed/GetFeed\?type=Calendar&unifiedId=[0-9]{5}&culture=[a-z]{2}-[A-Z]{2}&hash=[0-9a-z]{32}"

url = None

with open(conf, 'r') as file:
    lines = file.readlines()

    for line in lines:
        if line.startswith("url = "):
            existing_url = line.strip().split("= ")[1]
            if re.match(skoleintra_url_pattern, existing_url):
                url = existing_url
                break

if not url:
    while url is None:
        user_input = input("Enter the full URL from SkoleIntra: ")
        if re.match(skoleintra_url_pattern, user_input):
            url = user_input
        else:
            print("Invalid URL")

    with open(conf, 'w') as file:
        file.write(f"url = {url}\n")

subprocess.run(["wget", "-o", wget_log, "-O", feed_new, url])


# "--ignore-matching-lines=^DTSTAMP:................" is needed to ignore the timestamp of downloading since this changes every time you download the file
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