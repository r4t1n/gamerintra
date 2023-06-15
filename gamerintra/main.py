import subprocess
import sys
import time

url = input("Enter full URL from SkoleIntra: ")

# I could not get the tilda (~) to work so we use the username and full path instead
username = subprocess.check_output("whoami").decode(sys.stdout.encoding).strip()

location = "/home/" + username + "/.config/gamerintra/"
calendar_location = location + "calendar/"
log_location = location + "logs/"

feed = calendar_location + "GetFeed.ics"
feed_new = calendar_location + "GetFeed_new.ics"

current_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
wget_log = log_location + "wget_log_" + current_time

subprocess.run(["mkdir", "-p", calendar_location, log_location])
subprocess.run(["cp", "../gamerintra.conf", location])

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
    subprocess.run(["rm", feed_new])
elif diff_process.returncode == 1 or diff_process.returncode == 2:
    subprocess.run(["mv", feed_new, feed])
