from client import Client

def main():
  client = Client()
  client.connect()
  # Shutdown server
  # client.shutdown()

if __name__ == '__main__':
  main()