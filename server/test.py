import os
processes = os.popen('wmic process get description, processid, threadcount').read()
print(len(processes))

pid = input('Enter PID: ')
print(type(pid))
os.system(f'TASKKILL /PID {pid}')