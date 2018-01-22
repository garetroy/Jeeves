import discord
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
        self.add_command(self.register)
        self.add_command(self.points)
        self.add_command(self.flip)
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
    
    @commands.command(description="hi")
    async def hi(self):
        await self.say("hi")

    @commands.command()
    async def sumlvl(self,name=None):
        if(name == ""):
            await self.say("You must give me a name to lookup..")
            return
        await self.say("{}es level: {}"\
            .format(name, self.RI.summonerLevel(name)))

    @commands.command()
    async def lolV(self):
        version = self.RI.version
        await self.say("Leauge is in version {}".format(version))
        #need to test GET request here
        await self.say("https://na.leagueoflegends.com/en/news/game-updates" + \
            "/patch/patch-{}-notes".format(version[0:4].replace(".","")))

    @commands.command()
    async def lollast(self,name):
        msg = await self.say("```css\n Retreving data...```")
        st  = self.RI.returnLiveString(name)
        await self.edit_message(msg,st)
        #await self.say(msg.author)

    @commands.command()
    async def register(self,name=None):
        if(name == None):
            msg = self.messages[0]
            if(self.JUI.addUser(msg.author)):
                await self.say("Added")
            else:
                await self.say("You do not have permissions")
        else:
            try:
                user = self.get_user_info(name)
                if(self.JUI.addUser(user)):
                    await self.say("Added {}".format(str(user.name)))
                else:
                    await self.say("You do not have permissions")
            except discord.opus.NotFound:
                await self.say("Could not find user")
            else:
                await self.say("There was an error... Sorry")

    @commands.command()
    async def points(self,name=None):
        try:
            if(name == None):
                    user = self.messages[0].author
            else:
                    user = self.get_user_info(name)

            await self.say("```css\n You have {}  points```".format(\
                self.JUI.checkPoints(user)))
        except:
            await self.say("Could not find user...") 

    @commands.command()
    async def flip(self,guess=None,bet=None,opponent=None):
        if(guess == None):
            side = self.JUI.flipCoin()
        elif(bet == None):
            side = self.JUI.flipCoinGuess(guess)[1] 
        elif(bet != None and opponent !=None and guess != None):
            user = self.messages[0].author
            opp  = self.get_user_info(opponent)
            side = self.JUI.flipCoinBet(user,guess,bet,opp)
            await self.say("Something went wrong..")
            return

        await self.say(self.JUI.cssify(side))

    @commands.command()
    async def wiki(self,item):
        await self.say(wikipedia.summary(item))

if __name__ == '__main__':
    Jeeves.init()
