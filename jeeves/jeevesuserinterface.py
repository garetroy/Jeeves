from sys         import maxsize as maxint
from .jeevesuser import JeevesUser
from .games      import Games
from .errors     import *
from discord     import Member,utils

class JeevesUserInterface:
    """
        Represents a interface for the discord bot. 
        This class is used to communicate to the bot directly
        in essence funneling all functionality into it

    .. _discord.Role: https://discordpy.readthedocs.io/en/latest/api.html#discord.Role
    .. _discord.Member: https://discordpy.readthedocs.io/en/latest/api.html#discord.Member

    :class:`JeevesUserInterface` takes one argument.

    Parameters
    ----------
    adminrole : [`discord.Role`_]
        The admin role from the server. This is important to know so that
        the bot will always allow privliges to the admin.

    Attributes
    ----------
    games : (:class:`Games`)
        The games instance.
    
    adminrole : (`discord.Role`_)
        The administrator role given as a parameter for the server.
    """
    
    def __init__(self,adminrole):
        self.usersTable = {}
        self.games      = Games()
        self.adminrole  = adminrole

    def cssify(self,string):
        """
            Returns the string in css format for the discord bot
            so that it can properly format and color.

            Parameters
            -----------
            string : str
                The string that we want to cssify.

            Returns
            -------
            str
                The cssifyied string
        """
        return "```css\n{}```".format(string)

    def hasPermission(self, member, roles=[]):
        """
            This function checks if the `discord.member`_ has 
            sufficent permissions.
            
            Paramaters
            ----------
            member : `discord.Member`_
                The member we are going to check for permissions.
            roles  : Optional[`discord.Roles`_]
                The roles we are checking against. Admin is defined by default.

            Raises 
            -------
            ValueError
                Member instance was not passed in
            UserInsufficentPermissions
                The member did not have sufficent permissions      
        """
            
        if not isinstance(member, Member):
            raise ValueError
        
        #admin always there
        roles.append(self.adminrole)
        if(not any((i in roles) for i in member.roles)):
            raise UserInsufficentPermissions(member.name)

    def addUser(self, member, cmdfrom=None):
        if not isinstance(member, Member):
            raise ValueError

        if(cmdfrom != None and not isinstance(cmdfrom, Member)):
            raise ValueError

        #checks permissions for member, if cmdfrom declared
        #then it checks if cmdfrom has permissions to add the member instead
        #self.hasPermission(member if cmdfrom == None else cmdfrom)

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

    def getRole(self,msg,rolename):
        if(rolename == None):
            raise BadInput("Didn't specify a role")

        result = utils.get(msg.server.roles, name=rolename)
        if(result == None):
            raise BadInput("{} is not a vailid role".format(rolename))

        return result

    def register(self,name,msg,role):
        try:
            user = self.findName(msg.server,name)
            role = self.getRole(msg,role)

            self.hasPermission(msg.author)

            self.addUser(user,msg.author)
            return(user,role,"{} Added to {}".format(user.name,role.name))

        except UserNotAdded as err:
            return (err.message,)

        except UserInsufficentPermissions as err:
            return (err.message,)

        except BadInput as err:
            return (err.message,)

        except ValueError:
            return "Something went wrong..."
 
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
        self.usersTable[user1].points -= amount
        self.usersTable[user2].points += amount
         
    def flip(self,opponent,guess,bet,msg):
        if(guess == None):
            return self.games.flipCoin() 
        if(bet == None and guess == None):
            return self.games.flipCoinGuess(guess)[1]
        if(all(item is not None for item in [guess,bet,opponent,msg])):
            try:

                try:
                    bet = int(bet)
                except:
                    raise BadInput("Enter an integer for bet")

                member = msg.author
                opp    = self.findName(msg.server,opponent)
                
                #You have permission if you are in Games role
                #gamerole = self.getRole(msg,"Games")
                #self.hasPermission(member,[gamerole])

                opoints = self.checkPoints(opp)
                if(opoints < abs(int(bet))):
                    return "{} Has insufficant funds".format(opp.name)

                mpoints = self.checkPoints(member)
                if(mpoints < abs(int(bet))):
                    return "You insufficant funds".format(member.name)
                 
                result = self.games.flipCoinGuess(guess)

                if(result[0] == None):
                    return result[1]

                if(result[0]):
                    self.exchangePoints(opp,member,int(bet))
                else:
                    self.exchangePoints(member,opp,int(bet))

                string  = result[1] 
                string += "\n{} current balance:{}\n"
                string += "{} current balance:{}"
 
                return string.format(member.name,self.checkPoints(member),\
                    opp.name,self.checkPoints(opp))

            except UserNotAdded as err:
                return err.message

            except UserInsufficentPermissions as err:
                return err.message


            except BadInput as err:
                return err.message

            except ValueError:
                return "An error occured... Sorry"

        else:
            return "Invalid input"

    def points(self,name,msg):
        try:
            if(name == None):
                user = msg.author
                return "You have {} points.".format(self.checkPoints(user))
            else:
                user = self.findName(msg.server,name)
                return "{} has {} points".format(user.name,\
                    self.checkPoints(user))            
            
        except UserNotAdded as err:
            return err.message

        except UserInsufficentPermissions as err:
            return err.message 

        except ValueError:
            return "An error occured... Sorry"

    def flipStats(self):
        return "Heads: {}\nTails: {}".format(self.games.numheads,\
            self.games.numtails)

    def givePoints(self,msg,to,amount):
        try:
            try:
                amount = int(amount)
            except:
                raise BadInput("Please make the amount a positive integer")

            if(amount < 0):
                raise BadInput("Please make the amount a positve integer")

            member = msg.author
            opp    = self.findName(msg.server,to)

            mpoints = self.checkPoints(member)
            if(mpoints - abs(amount) < 0):
                return "You do not have enough to give away {} points"\
                    .format(mpoints)
            
            self.exchangePoints(member,opp,amount)

            return "Gave {} points to {}".format(amount,opp.name)

        except UserNotAdded as err:
            return err.message
        except UserInsufficentPermissions as err:
            return err.message
        except BadInput as err:
            return err.message
        except ValueError:
            return "An error occured... Sorry"
