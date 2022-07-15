import os
import time

start = time.time()
while True:
    if time.time() - start > 5:
        print("[ERROR] Timeout")
        break
    

