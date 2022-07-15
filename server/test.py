import tempfile

with tempfile.NamedTemporaryFile(suffix='.txt', delete=True) as file:
  file.write(b'Hello World')
  file.seek(0)
  print(file.read().decode())

