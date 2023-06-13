import subprocess
import sys

url = input("Enter full URL from skoleintra: ")
username = subprocess.check_output("whoami").decode(sys.stdout.encoding).strip()
location = "/home/" + username + "/.config/gamerintra"

subprocess.run(["mkdir", location])

subprocess.run(["wget", "--quiet", "-P", location, url])
