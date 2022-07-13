from client import Client

def main():
  client = Client()
  client.connect()
  client.run()

if __name__ == '__main__':
  main()