import subprocess
import time

while True:
    layquack_process = subprocess.Popen(['python', 'layquack.py'])
    time.sleep(100)
    layquack_process.terminate()
