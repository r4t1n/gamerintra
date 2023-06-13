import subprocess
import sys
import time

url = input("Enter full URL from SkoleIntra: ")

username = subprocess.check_output("whoami").decode(sys.stdout.encoding).strip()

location = "/home/" + username + "/.config/gamerintra/"
calendar_location = location + "calendar/"
log_location = location + "logs/"

subprocess.run(["mkdir", "-p", calendar_location, log_location])

current_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
subprocess.run(["wget", "-o", log_location + current_time, "-O", calendar_location + current_time, url])
