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
        self.add_command(self.flipStats)
        self.add_command(self.register)
        self.add_command(self.helpme)
        self.RI  = RiotInterface(self.riot)
        self.JUI = JeevesUserInterface()

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
        #await self.say(msg.author)

    @commands.command()
    async def register(self,name=None):
        msg = self.messages[0]
        gamerole = discord.utils.get(msg.server.roles, name="Games")
        if(name == None):
            if(self.JUI.addUser(msg.author)):
                await self.say("Added")
                await self.add_roles(msg.author,gamerole)
            else:
                await self.say("You do not have permissions")
        else:
            try:
                user = self.findName(msg.server,name)
                if(user == None):
                    raise ValueError

                if(not self.JUI.hasPermission(msg.author)):
                    await self.say("You do not have persmissions")
                    return

                if(self.JUI.addUser(user,permissions=True)):
                    await self.say("Added {}".format(user.name))
                    await self.add_roles(user,gamerole)
                else:
                    await self.say("You do not have permissions")

            except ValueError:
                await self.say("Could not find user {}".format(\
                        name))

    @commands.command()
    async def points(self,name=None):
        message = self.messages[0]
        try:
            if(name == None):
                user = message.author
                outstring = "You have {}  points".format(\
                    self.JUI.checkPoints(user))
                await self.say(outstring)
                return
            else:
                user = self.findName(message.server,name)

            if(user == None):
                await self.say("Could not find {}".format(name))
                return
            
            outstring = "{} has {} points".format(name,\
                self.JUI.checkPoints(user))

            await self.say(outstring)

        except KeyError as err:
            outstring = "{} is not registered to play games".format(user.name)
            await self.say(outstring)
            print(err)
        except ValueError as err:
            await self.say("Cannot find {}".format(name))
            print(err)

    @commands.command()
    async def flip(self,guess=None,bet=None, *, opponent=None):
        msg  =  self.messages[len(self.messages)-1]
        await self.say(self.JUI.flip(opponent,guess,bet,msg))

    @commands.command()
    async def flipStats(self):
        string = "Heads: {}\nTails: {}".format(self.JUI.numheads,\
                    self.JUI.numtails)
        await self.say(string)

    @commands.command()
    async def wiki(self,item):
        await self.say(wikipedia.summary(item))

    @commands.command()
    async def helpme(self):
            mem = self.messages[len(self.messages)-1].author
            await self.send_message(mem,"No I mean it, save me, you don't want"+\
                        " to know what he does during development") 

if __name__ == '__main__':
    Jeeves.init()
