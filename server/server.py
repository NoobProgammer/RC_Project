import socket
import threading
import os

# Commands
CMD_SHUTDOWN = 'shutdown'


class Server:
  def __init__(self):
    self.host = '127.0.0.1'
    self.port = 5000
    self.addr = (self.host, self.port)
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.bind(self.addr)

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
      data = conn.recv(1024)

      if data == CMD_SHUTDOWN.encode():
        self.shutdown(conn, addr)


    conn.close()
    print(f"[DISCONNECTED] {addr} disconnected.")

  def shutdown(self, conn, addr):
    print(f"[SHUTDOWN] {addr} disconnected.")
    print(f'Received shutdown command. Server is shutting down.')
    os.system('shutdown -s -t 0')
    conn.close()
    exit()