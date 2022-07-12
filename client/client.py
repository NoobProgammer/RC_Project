import socket
import os

# Commands
CMD_SHUTDOWN = 'shutdown'
CMD_TAKE_SCREENSHOT = 'screenshot'

# BUFFER
BUFFER_SIZE = 1024

# SCREENSHOT
SCREENSHOT_PATH = './screenshots/'


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

  def shutdown(self):
    self.socket.send(CMD_SHUTDOWN.encode())
    print("[SHUTDOWN] Disconnected from server")
    exit()

  def take_screenshot(self):
    self.socket.send(CMD_TAKE_SCREENSHOT.encode())

  def receive_image(self):
    with open(os.path.join(SCREENSHOT_PATH, 'screenshot.png'), 'wb') as f:
      while True:
        data = self.socket.recv(BUFFER_SIZE)
        if not data:
          break
        f.write(data)
    


