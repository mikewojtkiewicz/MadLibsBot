import subprocess
import sys
import time
import datetime
today = datetime.datetime.today().strftime('%Y-%m-%d')
failed = 0

while True:
    if failed == 10:
        sys.exit()
    print(str(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')) + ': MAD LIBS STARTING')
    subprocess.call([sys.executable, 'madlib.py'])
    print(str(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')) + ': MAD LIBS CRASHED')
    if datetime.datetime.today().strftime('%Y-%m-%d') == today:
        failed += 1
    else:
        failed = 1
        today = datetime.datetime.today().strftime('%Y-%m-%d')
    time.sleep(2)
    print(str(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')) + ': MAD LIBS RESTARTING')
