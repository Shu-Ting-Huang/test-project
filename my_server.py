import os
import time
import urllib.request

external_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
while True:
    os.system("python3 manage.py runserver --insecure " + external_ip + ":80")
    for i in reversed(range(1)):
        print(i+1)
        time.sleep(1)
