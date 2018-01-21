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
        self.add_command(self.lollast)
        self.add_command(self.wiki)
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
    async def lollast(self,name):
        global maps
        global matchtypes
        result = self.riotapi.getLiveMatch(name)
        matcht = matchtypes[str(result[2])]['string']
        red    = result[1]
        blue   = result[0]
        mapid  = maps[str(result[3])]['name']
        string  = "\n{:^50}\n".format("\----{}----\ ".format(matcht))
        string  += "\n{:^50}\n\n".format("\----{}----\ ".format(mapid))
        pattern = "{:<10}{:^3}{:^10}{:^3}{:^8}\n\n"
        string += pattern.format("Participants", "|", "Champion", "|", "Team")
        for i in red:
            string += i + (" "*(16-len(i)))
            string += red[i][0] + (" "*(14 - len(red[i][0])))
            string += "Red\n"
        string += "\n"
        for i in blue:
            string += i + (" "*(16-len(i)))
            string += blue[i][0] + (" "*(14-len(blue[i][0])))
            string += "Blue\n"

        string =  "```" + string + "```"

        await self.say(string)
    
    @commands.command()
    async def wiki(self,item):
        await self.say(wikipedia.summary(item))

if __name__ == '__main__':
    global maps
    global matchtypes
    with open('gameconstants.json', 'r') as jsonf:
        all_ = json.load(jsonf,strict=False)
        maps = all_['maps']
        matchtypes = all_['queuestypes']
    Jeeves.init()
