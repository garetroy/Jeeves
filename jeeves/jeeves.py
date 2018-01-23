import discord, asyncio
import json
import wikipedia
from riotinterface import RiotInterface
from jeevesuserinterface import JeevesUserInterface
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
        self.add_command(self.points)
        self.add_command(self.flip)
        self.add_command(self.flipstats)
        self.add_command(self.register)
        self.add_command(self.give)
        self.RI        = RiotInterface(self.riot)
        self.JUI       = None

    @property
    def token(self):
        with open('../data/info.json', 'r') as jsonf:
            return json.load(jsonf)['token']
    
    @property
    def riot(self):
        with open('../data/info.json', 'r') as jsonf:
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
        self.adminrole = discord.utils.get(list(self.servers)[0]\
            .roles, name="Gods")
        self.JUI = JeevesUserInterface(self.adminrole)

    def say(self,*args,**kwargs):
        
        if(type(args[0]) != bool):
            args = (True,) + args #setting cssify to true (making default)

        if(args[0]):
            temp  = self.JUI.cssify(args[1])
            args  = (temp,)
        else:
            args  = (args[1],)
        for i in range(2,len(args)):
            args += args[i]

        return super().say(*args,**kwargs)
        
    @commands.command(description="hi")
    async def hi(self):
        await self.say("hi")

    @commands.command()
    async def sumlvl(self,name=None):
        if(name == ""):
            await self.say("You must give me a name to lookup..")
            return
        await self.say("{} level: {}"\
            .format(name, self.RI.summonerLevel(name)))

    @commands.command()
    async def lolV(self):
        version = self.RI.version
        await self.say("Leauge is in version {}".format(version))
        #need to test GET request here
        await self.say(False,\
            "https://na.leagueoflegends.com/en/news/game-updates" +\
            "/patch/patch-{}-notes".format(version[0:4].replace(".","")))

    @commands.command()
    async def lollast(self,name):
        msg = await self.say("```css\n Retreving data...```")
        st  = self.RI.returnLiveString(name)
        await self.edit_message(msg,st)

    @commands.command(pass_context=True)
    async def register(self,ctx, name, *, role=None):
        msg = ctx.message
        results = self.JUI.register(name,msg,role)
        if(len(results) == 1):
            await self.say(results[0])
            return

        await self.add_roles(results[0],results[1])
        await self.say(results[2])

    @register.error
    async def register_error(self,ctx,error):
        await self.say("Invalid input")

    @commands.command(pass_context=True)
    async def points(self,ctx,*,name=None):
        msg = ctx.message
        await self.say(self.JUI.points(name,msg))

    @commands.command(pass_context=True)
    async def flip(self,ctx,guess=None,bet=None, *, opponent=None):
        msg  = ctx.message
        await self.say(self.JUI.flip(opponent,guess,bet,msg))

    @commands.command()
    async def flipstats(self):
        await self.say(self.JUI.flipStats())

    @commands.command()
    async def wiki(self,item):
        await self.say(wikipedia.summary(item))

    @commands.command(pass_context=True)
    async def give(self,ctx,to,amount):
        msg = ctx.message
        await self.say(self.JUI.givePoints(msg,to,amount))

if __name__ == '__main__':
    Jeeves.init()
