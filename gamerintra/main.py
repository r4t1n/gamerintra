import subprocess
import sys
import time

url = input("Enter full URL from SkoleIntra: ")
username = subprocess.check_output("whoami").decode(sys.stdout.encoding).strip()
calendar_location = "/home/" + username + "/.config/gamerintra/calendar/"

subprocess.run(["mkdir", "-p", calendar_location])

current_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
subprocess.run(["wget", "--quiet", "-O", calendar_location + current_time, url])
