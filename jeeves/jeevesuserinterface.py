from jeevesuser import JeevesUser
from random import randrange

class JeevesUserInterface:
    
    def __init__(self):
        self.usersTable = {}
        self.numheads   = 0
        self.numtails   = 0

    def cssify(self,string):
        return "```css\n{} ```".format(string)

    def addUser(self, user):
        if not self.hasPermission(user):
            return False

        if user in self.usersTable:
            return True

        ju = JeevesUser(user)
        if(user.nick != None):
            ju.callme = (user.nick, True)

        self.usersTable[user] = ju

        return True
         
    def checkPoints(self, user):
        if(user not in self.usersTable):
            if(self.addUser(user)):
                return self.usersTable[user].points

            raise ValueError
        else:
            return self.usersTable[user].points

    def exchangePoints(self, user1, user2, points):
        self.addUser(user1)
        self.addUser(user2)
        self.usersTable[user1].points -= points
        self.usersTable[user2].points += points
    
    def hasPermission(self, user):
        print(user.roles)
        roles = [str(i) for i in user.roles]
        if("Games" not in roles or "Gods" not in roles):
            return False
        return True

    def flipCoin(self,debug=None):
        val =  randrange(0,2) if debug == None else debug
        if(val == 0):
            self.numheads += 1
            return 'heads'
        else:
            self.numtails += 1
            return 'tails'

    def flipCoinGuess(self,guess):
        side = self.flipCoin()
        if(side == guess.lower()):
            return (True, "It was {}! You won.".format(side))
        return (False,"It was {}! You lose.".format(side))

    def flipCoinBet(self,user,guess,amount,opp):
        isGod = "Gods" in [str(i) for i in user.roles]
        if(not isGod and not self.hasPermission(user)):
            return "Sorry, you don't have permissions to bet"
        
        if(not isGod and (self.checkPoints(user)-amount) < 0 and \
                (self.checkPoints(opp)-amount) < 0):
            return "Sorry you or the opponent don't have sufficent funds."

        result = self.flipCoinGuess(guess)
        if(result[0]):
            self.exchangePoints(opp,user,int(amount))
        else:
            self.exchangePoints(user,user,int(amount))
        string  = result[1] 
        string += "\n{} current balance:{}\n".format(\
            user.name,self.checkPoints(user))
        string += "{} current balance:{}".format(\
            opp.name,self.checkPoints(opp))

        return string
            
