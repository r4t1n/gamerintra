import subprocess
import sys
import time

url = input("Enter full URL from SkoleIntra: ")

# I could not get the tilda (~) to work so we use the username and full path instead
username = subprocess.check_output("whoami").decode(sys.stdout.encoding).strip()

location = "/home/" + username + "/.config/gamerintra/"
calendar_location = location + "calendar/"
log_location = location + "logs/"

feed = "GetFeed.ics"
feed_new = "GetFeed_new.ics"

subprocess.run(["mkdir", "-p", calendar_location, log_location])
subprocess.run(["cp", "../gamerintra.conf", location])

current_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
subprocess.run(["wget", "-o", log_location + "wget-log_" + current_time, "-O", calendar_location + feed_new, url])

# "--ignore-matching-lines=^DTSTAMP:................" is needed to ignore the timestamp of downloading since this changes every time you download the file
# We use "stdout=subprocess.DEVNULL" and "stderr=subprocess.DEVNULL" since I do not want diff printing out "No such file or directory" if you run the script for the first time
diff_process = subprocess.run(
    ["diff", "-q", "--ignore-matching-lines=^DTSTAMP:................", calendar_location + feed_new, calendar_location + feed],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# Return code 0 = The files are identical
# Return code 1 = The files are not identical
# Return code 2 = No such file or directory
if diff_process.returncode == 0:
    subprocess.run(["rm", calendar_location + feed_new])
elif diff_process.returncode == 1:
    subprocess.run(["mv", calendar_location + feed_new, calendar_location + feed])
elif diff_process.returncode == 2:
    subprocess.run(["mv", calendar_location + feed_new, calendar_location + feed])
