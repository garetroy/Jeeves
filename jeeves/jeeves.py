import discord, asyncio
import json
import wikipedia
import glob
from os                   import listdir
from os.path              import join,isfile
from .riotinterface       import RiotInterface
from .jeevesuserinterface import JeevesUserInterface
from .db                  import DB
from discord.ext          import commands

description        = "? to use me ;)"
startup_extensions = [f"jeeves.cogs.{ext[:-3]}" \
                for ext in glob.glob("src/discord/*.py")]
                

class Jeeves(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="?", description=description,
            pm_help=None) 
        self.add_command(self.hi)
#        self.add_command(self.sumlvl)
#        self.add_command(self.lolV)
#        self.add_command(self.lollast)
#        self.add_command(self.wiki)
        self.add_command(self.points)
        self.add_command(self.flip)
        self.add_command(self.flipstats)
        self.add_command(self.rollstats)
        self.add_command(self.botstats)
#        self.add_command(self.register)
        self.add_command(self.give)
        self.add_command(self.roll)
        self.RI        = RiotInterface(self.riot)
        self.JUI       = None
        self.db        = None

    @property
    def token(self):
        with open('./data/info.json', 'r') as jsonf:
            return json.load(jsonf)['token']
    
    @property
    def riot(self):
        with open('./data/info.json', 'r') as jsonf:
            return json.load(jsonf)['riot']

    @classmethod
    def init(bot):
        bot = Jeeves()
        #load cogs
        for extension in startup_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.')
                traceback.print_exc()
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
        self.JUI    = JeevesUserInterface(self.adminrole)
        self.db     = DB(self.JUI.hasPermission)
        self.JUI.db = self.db 

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
        
    description = "Jeeves greets you."
    @commands.command(description=description,brief=description)
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
        results = self.JUI.register(ctx,name,role)
        if(len(results) == 1):
            await self.say(results[0])
            return

        await self.add_roles(results[0],results[1])
        await self.say(results[2])

    @register.error
    async def register_error(self,ctx,error):
        await self.say("Invalid input")

    description = "Shows either your own or someone elses points."
    longdesc    = "Name : Optional parameter of who's points you want to look up."
    @commands.command(pass_context=True,brief=description,description=longdesc)
    async def points(self,ctx,*,name=None):
        await self.say(self.JUI.points(ctx,name))

    description = "Flips a coin, can take a guess, can bet against people."
    longdesc    = description + "\nguess: Optional, the guess if the flip" + \
                 " will be heads or tails. (Use 'heads' or 'tails')." +\
                 "\nbet: The amount you want to wager against an opponent." + \
                 "\nopponent: The name of the person you want to bet against."
    @commands.command(pass_context=True,brief=description,description=longdesc)
    async def flip(self,ctx,guess=None,bet=None, *, opponent=None):
        await self.say(self.JUI.flip(ctx,opponent,guess,bet))

    description = "Rolls dice, telling you what Jeeves rolled."
    @commands.command(pass_context=True,brief=description,description=description)
    async def roll(self):
        await self.say(self.JUI.roll())

    async def roll_error(self,ctx,error):
        await self.say(error.message)

    description = "Shows you coin flipping stats."
    @commands.command(brief=description,description=description)
    async def flipstats(self):
        await self.say(self.JUI.flipStats())

    description = "Shows you dice rolling stats."
    @commands.command(brief=description,description=description)
    async def rollstats(self):
        await self.say(self.JUI.rollStats())

    description = "Shows you the stats of Jeeves."
    @commands.command(description=description, brief=description)
    async def botstats(self):
        await self.say(self.JUI.serverStats())

    @commands.command()
    async def wiki(self,item):
        await self.say(wikipedia.summary(item))

    description = "Allows you to give your points to someone."
    longdesc    = "Allows you to give your points to someone.\n" + \
                 "amount : Amount you want to give.\n"+\
                 "to: Name of who you want to gift."
    @commands.command(pass_context=True,brief=description,description=longdesc)
    async def give(self,ctx,amount,*,to):
        await self.say(self.JUI.givePoints(ctx,amount,to))

if __name__ == '__main__':
           Jeeves.init()
