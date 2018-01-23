from sys        import maxsize as maxint
from jeevesuser import JeevesUser
from random     import randrange
from discord    import Member

class JeevesUserInterface:
    
    def __init__(self):
        self.usersTable = {}
        self.numheads   = 0
        self.numtails   = 0
        self.debugnum   = None

    def cssify(self,string):
        return "```css\n{}```".format(string)

    def addUser(self, member, permissions=False):
        if not isinstance(member, Member):
            raise ValueError

        if not self.hasPermission(member) and not permissions:
            return False

        if member in self.usersTable:
            return True

        ju = JeevesUser(member)
        if(member.nick != None):
            ju.callme = (member.nick, True)

        self.usersTable[member] = ju
        return True

    def findName(self,server,name):
        mem = server.get_member_named(name)

        if(mem == None):
            mem = ''.join(i for i in name if i.isdigit())
            mem = server.get_member(mem)
    
        return mem 
         
    def checkPoints(self, member):
        if not isinstance(member, Member):
            raise ValueError

        if(member not in self.usersTable):
            if(self.addUser(member)):
                return self.usersTable[member].points
            raise KeyError
        else:
            return self.usersTable[member].points

    def exchangePoints(self, user1, user2, amount):
        self.addUser(user1)
        self.addUser(user2)
        if(amount >= maxint):
            self.usersTable[user1].points = -maxint
            self.usersTable[user2].points = maxint
        else: 
            self.usersTable[user1].points = (self.usersTable[user1].points \
                - amount) % -maxint
            self.usersTable[user2].points = (self.usersTable[user2].points \
                + amount) % maxint
    
    def hasPermission(self, member):
        if not isinstance(member, Member):
            raise ValueError

        roles = [str(i) for i in member.roles]
        if("Games" not in roles and "Gods" not in roles):
            return False
        return True

    def flipCoin(self):
        val =  randrange(0,2) if self.debugnum == None else self.debugnum
        if(val == 0):
            self.numheads += 1
            return 'heads'
        else:
            self.numtails += 1
            return 'tails'

    def flipCoinGuess(self,guess):
        side = self.flipCoin()

        if('s' not in guess): #head->heads, tail->tails
            guess += 's'

        if(guess.lower() not in ['heads','tails']):
            return (None, "Please use heads or tails")

        if(side == guess.lower()):
            return (True, "It was {}! You won.".format(side))
        return (False,"It was {}! You lost.".format(side))

    def flipCoinBet(self,member,opp,guess,amount):
        if not isinstance(member, Member) or not isinstance(opp, Member):
            raise ValueError

        isGod = "Gods" in [str(i) for i in member.roles]
        if(not self.hasPermission(member)):
            return "Sorry, you don't have permissions to bet"
        elif(not self.hasPermission(opp) and isGod):
            self.addUser(opp,permissions=True)
        
        if(not isGod and (self.checkPoints(member)-amount) < 0 and \
                (self.checkPoints(opp)-amount) < 0):
            return "Sorry you or the opponent does not have sufficent funds."

        result = self.flipCoinGuess(guess)
        if(result[0] == None):
            return result[1]

        if(result[0]):
            self.exchangePoints(opp,member,int(amount))
        else:
            self.exchangePoints(member,opp,int(amount))
        string  = result[1] 
        string += "\n{} current balance:{}\n".format(\
            member.name,self.checkPoints(member))
        string += "{} current balance:{}".format(\
            opp.name,self.checkPoints(opp))

        return string
            
    def flip(self,opponent,guess,bet,msg=None):
        if(guess == None):
            return self.flipCoin() 
        if(bet == None):
            return self.flipCoinGuess(guess)[1]
        if(all(item is not None for item in [guess,bet,opponent,msg])):
            try:
                bet = int(bet)
            except:
                return "Use an integer for your bet {}".format(msg.author) 

            try:
                member = msg.author
                opp    = self.findName(msg.server,opponent)

                if(opp == None):
                    return "Could not find {}".format(opponent)
    
                return self.flipCoinBet(member,opp,guess,amount)                 

            except KeyError:
                return "{} was not registered, or does not have correct" + \
                        " permissions".format(member.name)

            except ValueError:
                return "Cannot find {} or {}".format(member.name,opponent)

        return ""

