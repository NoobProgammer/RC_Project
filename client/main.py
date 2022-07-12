from client import Client

def main():
  client = Client()
  client.connect()
  client.take_screenshot()
  client.receive_image()
  # Shutdown server
  # client.shutdown()

if __name__ == '__main__':
  main()