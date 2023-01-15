# SepticX 🐀

An advanced python Rat Client capable of many malicious tasks

![image](https://user-images.githubusercontent.com/78031685/212566138-bd9d66f5-0225-4219-a883-7e6b22231840.png)


# Features

This tool is able to do all of these tasks, all at once

 - Completely FUD
 - Add's to startup
 - Trollware
 - File encryption for ransomware
 - Auto Spread's through discord
 - KeyLogging
 - Reverse Shell (Liscense Required)
 - Spyware accessing, camera, and screen display (Liscense Required)
 - Disable CMD, Registry Editor, TaskMGR, as well as all of the Power buttons including, shut off, restart and sleep
 - Disables Windows Defender
 - Incredibly Accurate VM Detection
 - Bypasses VirusTotal
 - Grab's all of Browser credentials, including, Passwords, Cookies, Browser History, and Payment Methods
 - Constantly searches for processes like `Process Hacker` or `Wire Shark` and closes them immideatly
 - Grab's Discord token's, and Roblox cookies

# Setup

Setup can be done pretty quickly!<br>
 - Upload the contents of the server folder into replit
 - Copy and paste example.json into the replit secret manager to set the `ENV` variables, Remember to replace the env variables with your own information
    - For the `key` variable go to <a src="https://emn178.github.io/online-tools/sha256.html">this link</a> and input whatever password you want, copy the output then set the `ENV` variable to the output from the site 
        - This is the same key you will use when building the rat

    - For `t` replace it with your a discord token, so it can dynamically

    - `webhook_generation_logs` is the channel where the log of all webhooks being generated will go and `backup_webhook` is a backup token incase it fails to create a webhook

 - On the replit on main.py there will be two variables called `channel_id` and `channel_id2` set them to two different discord channel id's so incase one has a ratelimit the log is still sent

 - Once you've setup your replit, run compiler.py, and either put your config inside config.json and use that or type in your config manually

- Inside your replit replace main.exe with the stub you created with compiler.py, and logger.exe with whatever file you want, like a crypto miner for example

 - Then run it on a target machine and it should connect

 - To see your keylogs check the logs folder on the replit, everything else will be sent to your discord webhook and finally run `Controller.py` to control any connected clients

![image](https://user-images.githubusercontent.com/78031685/212566168-1d2ab61c-843b-4c2b-9ad9-48fc915788de.png)


### Extra

If you go into the `src\files` directory you'll find some files that the Rat load will put onto their pc when the Ransomware runs

If you want you can change wallpaper.jpg and annoy.mp3 to whatever you want. Just keep the filenames the same

For Instructions.txt you can also change it to whatever you want but, if you want instead of putting your wallet address and the amount of money into the file you can use `WALLET` and `AMOUNT` and the program will automatically replace them

# Getting a License

This is only the Open Source version of the client, if you'd like to gain access to the more advanced features like, better obfuscation go to the Offical <a src="https://discord.gg/CFfTAYHyq5">Discord Server</a>

# Support
If you you'd like to report any bugs or ask for support go to my <a src="https://discord.gg/CFfTAYHyq5">Discord Server</a>

# Disclaimer

Do not use this tool to remotely access anyone's computer with their consent, for that is illegal by federal law.
