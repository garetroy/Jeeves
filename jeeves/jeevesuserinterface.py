from sys        import maxsize as maxint
from jeevesuser import JeevesUser
from games      import Games
from errors     import *
from discord    import Member,utils

class JeevesUserInterface:
    
    def __init__(self):
        self.usersTable = {}
        self.games      = Games()

    def cssify(self,string):
        return "```css\n{}```".format(string)

    def addUser(self, member, permissions=False):
        if not isinstance(member, Member):
            raise ValueError

        if not self.hasPermission(member) and not permissions:
            raise UserInsufficentPermissons(member.name)

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
    
        if(mem == None):
            raise UserNotAdded(name)

        return mem 
         
    def checkPoints(self, member):
        if not isinstance(member, Member):
            raise ValueError

        if(member not in self.usersTable):
            if(self.addUser(member)):
                return self.usersTable[member].points
            raise UserNotAdded(member.name)
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
    
    def hasPermission(self, member, roles=[]):
        if not isinstance(member, Member):
            raise ValueError
        
        roles.append("Gods")
        if(any(i in roles for i in member.roles)):
            return False
        return True
        #NEED TO FIX SO IT RAISES ERRORS

    def register(self,name,msg,role):
        try:
            if(name == None):
                user = msg.author
            else:
                user = self.findName(msg.server,name)

            self.addUser(user)
            return(user,role,"{} Added to {}".format(user.name,role.name))

        except UserNotAdded as err:
            return err.message

        except UserInsufficentPermissions as err:
            return err.message

        except ValueError:
            return "Something went wrong..."
          
    def flip(self,opponent,guess,bet,msg):
        if(guess == None):
            return self.games.flipCoin() 
        if(bet == None):
            return self.games.flipCoinGuess(guess)[1]
        if(all(item is not None for item in [guess,bet,opponent,msg])):
            try:
                bet = int(bet)
            except:
                return "Use an integer for your bet {}".format(msg.author) 

            try:
                member = msg.author
                opp    = self.findName(msg.server,opponent)
                
                if(not self.hasPermission(member)): #REMOVE AFTER PERMISSION FIX
                    return "You don't have sufficent Permissions"
                
                #CHECK POINT BALANCE

                result = self.games.flipCoinBet(member,opp,guess,bet)
                if(result[0] == None):
                    return result[1]

                if(result[0]):
                    self.exchangePoints(opp,member,int(bet))
                else:
                    self.exchangePoints(member,opp,int(bet))

                return result[1].format(member.name,self.checkPoints(member),\
                    opp.name,self.checkPoints(opp))

            except UserNotAdded as err:
                return err.message

            except UserInsufficentPermissions as err:
                return err.message

            except ValueError:
                return "An error occured... Sorry"

    def points(self,name,msg):
        try:
            if(name == None):
                user = msg.author
                return "You have {} points.".format(self.checkPoints(user))
            else:
                user = self.findName(msg.server,name)
                return "{} has {} points".format(user.name,self.checkPoints(user))            
            
        except UserNotAdded as err:
            return err.message

        except UserInsufficentPermissions as err:
            return err.message 

        except ValueError:
            return "An error occured... Sorry"

    def flipStats(self):
            return "Heads: {}\nTails: {}".format(self.games.numheads,\
                self.games.numtails)

