import tkinter as tk
import threading
from server import Server

event = threading.Event()

def start_server(server):
  thread = threading.Thread(target=server.run, args=(event,), daemon=True)
  thread.start()

def stop_server(root):
  # Kill server thread
  print('[SHUTDOWN] Stopping server...')
  event.set()
  root.destroy()

if __name__ == '__main__':
  root = tk.Tk()
  root.title("Server")
  root.geometry("200x100")

  # Create server instance
  server = Server()

  # Create button
  start_btn = tk.Button(root, text="Start server", command=lambda: start_server(server))
  start_btn.pack()

  exit_btn = tk.Button(root, text="Exit", command=lambda: stop_server(root))
  exit_btn.pack()

  root.mainloop()