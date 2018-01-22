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
        self.add_command(self.points)
        self.add_command(self.flip)
        self.add_command(self.flipStats)
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
        await self.say("https://na.leagueoflegends.com/en/news/game-updates" +\
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
        message = self.messages[0]
        try:
            if(name == None):
                    user = message.author
            else:
                    user = message.server.get_member_named(name)
                    if(user == None):
                        user = message.server.get_member(name)

            outstring = "You have {}  points".format(self.JUI.checkPoints(user))
            await self.say(self.JUI.cssify(outstring))
        except KeyError as err:
            outstring = "{} is not registered to play games".format(user.name)
            await self.say(self.JUI.cssify(outstring))
            print(err)
        except ValueError as err:
            await self.say(self.JUI.cssify("@garett -- points"))
            print(err)

    @commands.command()
    async def flip(self,guess=None,bet=None, *, opponent=None):
        side = ""
        msg  =  self.messages[0]
        if(guess == None):
            side = self.JUI.flipCoin()
        elif(bet == None):
            side = self.JUI.flipCoinGuess(guess)[1] 
        elif(bet != None and opponent !=None and guess != None):
            try:
                bet = int(bet) 
            except:
                await self.say("Use a integer for your bet...")
                return
            try:
                member = msg.author
                opp    = msg.server.get_member_named(opponent)
                if(opp == None):
                    opponent = ''.join(i for i in opponent if i.isdigit())
                    opp = msg.server.get_member(opponent)
                side   = self.JUI.flipCoinBet(member,opp,guess,bet)

            except KeyError as err:
                side = "{} does not have correct permissions".format(\
                    member.name)
                print(err)
            except ValueError as err:
                side = "@garett -- flip"
                print(err)

        await self.say(self.JUI.cssify(side))

    @commands.command()
    async def flipStats(self):
        string = "Heads: {}\nTails: {}".format(self.JUI.numheads,\
                    self.JUI.numtails)
        await self.say(self.JUI.cssify(string))

    @commands.command()
    async def wiki(self,item):
        await self.say(wikipedia.summary(item))

if __name__ == '__main__':
    Jeeves.init()
