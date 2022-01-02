import os
import time
while True:
    os.system("python3 manage.py runserver")
    for i in reversed(range(5)):
        print(i+1)
        time.sleep(1)
