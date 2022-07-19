import os

apps = os.popen(
    'powershell "gps | where {$_.MainWindowTitle } | select ProcessName, Id').read()
print(apps)
