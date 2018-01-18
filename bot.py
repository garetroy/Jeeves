import discord
from discord.ext import commands
import json

description = "? to use me ;)"

class Jeeves(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="?", description=description,
            pm_help=None) 
        self.add_command(self.hi)

    @property
    def token(self):
        with open('info.json', 'r') as jsonf:
            return json.load(jsonf)['token']

    @classmethod
    def init(bot):
        bot = Jeeves()
        try:
            bot.run(bot.token, reconnect=True)
        except Exception as e:
            print(e)
        
    async def on_ready(self):
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("--Channels--")
        for channel in self.get_all_channels():
            print("name:{} id:{} type:{}".format(channel,channel.id,channel.type))

    @commands.command()
    async def hi(self):
        await self.say("hi")

if __name__ == '__main__':
    Jeeves.init()
