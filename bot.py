import discord
import json
import wikipedia
from riotapi     import Riot
from discord.ext import commands

description = "? to use me ;)"

class Jeeves(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="?", description=description,
            pm_help=None) 
        self.add_command(self.hi)
        self.add_command(self.sumlvl)
        self.add_command(self.lolV)
        self.add_command(self.lollive)
        self.riotapi = Riot(self.riot)

    @property
    def token(self):
        with open('info.json', 'r') as jsonf:
            return json.load(jsonf)['token']
    
    @property
    def riot(self):
        with open('info.json', 'r') as jsonf:
            return json.load(jsonf)['riot']

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
    
    @commands.command(description="hi")
    async def hi(self):
        await self.say("hi")

    @commands.command()
    async def sumlvl(self,name=None):
        if(name == None):
            await self.say("You must give me a name to lookup..")
            return
        await self.say("{}es level: {}"\
            .format(name, self.riotapi.summonerLevel(name)))

    @commands.command()
    async def lolV(self):
        version = self.riotapi.version
        await self.say("Leauge is in version {}".format(version))
        #need to test GET request here
        await self.say("https://na.leagueoflegends.com/en/news/game-updates" + \
            "/patch/patch-{}-notes".format(version[0:4].replace(".","")))

    @commands.command()
    async def lollive(self,name):
        await self.say(self.riotapi.getLiveMatch(name))
    
    @commands.command()
    async def wiki(self,item):
        await self.say(wikipedia.summary(item))

if __name__ == '__main__':
    Jeeves.init()
