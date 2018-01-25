from .db         import DB
from .jeevesuser import JeevesUser
from .games      import Games
from .errors     import *
from discord     import Member,utils
from sys         import maxsize as maxint

class JeevesUserInterface:
    """
        Represents a interface for the discord bot. 
        This class is used to communicate to the bot directly
        in essence funneling all functionality into it

        .. _discord.Role: https://discordpy.readthedocs.io/en/latest/api.html#discord.Role
        .. _discord.Member: https://discordpy.readthedocs.io/en/latest/api.html#discord.Member
        .. _discord.Server: https://discordpy.readthedocs.io/en/latest/api.html#discord.Server

    :class:`JeevesUserInterface` takes one argument.

    Parameters
    -----------
    adminrole : [`discord.Role`_]
        The admin role from the server. This is important to know so that
        the bot will always allow privliges to the admin.

    Attributes
    ----------
    games     : (:class:`Games`)
        The games instance.
    
    adminrole : (`discord.Role`_)
        The administrator role given as a parameter for the server.
    """
    def __init__(self,adminrole):
        self.db         = None
        self.games      = Games()
        self.adminrole  = adminrole

    def cssify(self,string):
        """
            Returns the string in css format for the discord bot
            so that it can properly format and color.

            Parameters
            -----------
            string : (str)
                The string that we want to cssify.

            Returns
            -------
            **Returns** the cssifyied string.
        """
        return "```css\n{}```".format(string)

    def hasPermission(self, member, roles=[]):
        """
            This function checks if the `discord.member`_ has 
            sufficent permissions.
            
            Parameters
            ----------
            member : (`discord.Member`_)
                The member we are going to check for permissions.

            roles  : Optional[`discord.Role`_]
                The roles we are checking against. Admin is added automatically.

            Raises 
            -------
            InvalidInput 
                member was not a `discord.Member`_ instance.

            UserInsufficentPermissions
                The member did not have sufficent permissions.
        """
        if not isinstance(member, Member):
            raise InvalidInput(type(member),type(Member),"jui.hasPersmission")
        
        #admin always there
        roles.append(self.adminrole)
        if(not any((i in roles) for i in member.roles)):
            raise UserInsufficentPermissions(member.name)

    def findName(self,server,name):
        """
            Finds the name in the given server, then returning the 
            `discord.Member`_ associated with the name.
        
            Parameters
            ----------
            server : (`discord.Server`_)
                The server we want to search for the name in.

            name   : (str)
                The string representing the name we want to search for.
        
            Raises
            -------
            UserNotAdded
                If we cannot find the name in the server.

            Returns
            --------
            **Returns** `discord.Member`_.
        """
        mem = server.get_member_named(name)

        if(mem == None):
            mem = ''.join(i for i in name if i.isdigit())
            mem = server.get_member(mem)
    
        if(mem == None):
            raise UserNotAdded(name)

        return mem 

    def getRole(self,server,rolename):
        """
            Gets the role from the given server.

            Parameters
            ----------
            server   : (`discord.Server`_)
                The server we want to search for the given role in.

            rolename : (str)
                The name of the role we want to search for.

            Raises
            ------
            BadInput
                If there is an invalid or role was not specified

            Returns
            -------
            **Returns** the desired `discord.Role`_
        """
        if not isinstance(type(server),Server):
            raise InvalidType(type(server),type(Server),"JUI.getRole")

        if(rolename == None):
            raise BadInput("Didn't specify a role")

        result = utils.get(server.roles, name=rolename)
        if(result == None):
            raise BadInput("{} is not a vailid role".format(rolename))

        return result

    def register(self,ctx,name,role):
        """
            Registers the given name with the role from the context.
            
            Parameters
            -----------
            ctx  : (discord.ext.Context)
                The context given from discord bot.

            name : (str)
                The name of the member we want to change.

            role : (str)
                The role we want to move the member into.
        
            Returns
            -------
            **Returns** a str. Describes the success if successful. If not
            it returns the error message.
        """ 
        try:
            user = self.findName(msg.server,name)
            role = self.getRole(msg.server,role)

            self.hasPermission(msg.author)

            self.addUser(user,msg.author)
            return(user,role,"{} Added to {}".format(user.name,role.name))

        except UserNotAdded as err:
            return (err.message,)

        except UserInsufficentPermissions as err:
            return (err.message,)

        except BadInput as err:
            return (err.message,)

        except InvalidType as err:
            print(err.message)
            return "Something went wrong..."
 
    def flip(self,ctx,opponent,guess,bet):
        """
            A wrapper function for the `Games` role modules in order
            to place bets based on a coin flip. (or just flip a coin).
            If no guess is specified, then it will just flip the coin.
            If no opponent or bet is specified, and guess is, then it
            will flip the coin with the guess in mind.

            Parameters
            ----------
            ctx      : (discord.ext.Context)
                The context given from discord bot.
            
            opponent : Optional[`discord.Member`_]
                The member we want to bet against.

            guess    : Optional[str]
                This should be a string containing "heads" or "tails".
            
            bet      : (int)
                The amount that the individual wants to bet. You can
                bet against yourself (by going negitive). 

            Returns
            -------
            **Returns** a corresponding string, depending on the above options
            if there is an error, it will print the string error.
         
        """ 
        if(guess == None):
            flip = self.games.flipCoin()
            self.db.changeFlipStats(flip)
            return flip
        if(bet == None and guess == None):
            flip = self.games.flipCoinGuess(guess)
            self.db.changeFlipStats(flip[2]) 
            return flip[1]
        if(all(item is not None for item in [guess,bet,opponent])):
            try:

                try:
                    bet = int(bet)
                except:
                    raise BadInput("Enter an integer for bet")

                member = ctx.message.author
                opp    = self.findName(ctx.message.server,opponent)
                
                #You have permission if you are in Games role
                #gamerole = self.getRole(msg.server,"Games")
                #self.hasPermission(member,[gamerole])

                opoints = self.db.checkPoints(opp)
                if(opoints < abs(int(bet))):
                    return "{} Has insufficant funds".format(opp.name)

                mpoints = self.db.checkPoints(member)
                if(mpoints < abs(int(bet))):
                    return "You insufficant funds".format(member.name)
                 
                result = self.games.flipCoinGuess(guess)
                self.db.changeFlipStats(result[2])

                if(result[0]):
                    self.db.exchangePoints(opp,member,int(bet))
                else:
                    self.db.exchangePoints(member,opp,int(bet))

                string  = result[1] 
                string += "\n{} current balance:{}\n"
                string += "{} current balance:{}"
 
                return string.format(member.name,self.db.checkPoints(member),\
                    opp.name,self.db.checkPoints(opp))

            except UserNotAdded as err:
                return err.message

            except UserInsufficentPermissions as err:
                return err.message

            except BadInput as err:
                return err.message

            except InvalidType as err:
                print(err.message)
                return "An error occured... Sorry"

        else:
            return "Invalid input"

    def points(self,ctx,name=None):
        """
            Checks the points of the person who asked, or the name specified.
        
            Parameters
            ----------
            ctx  : (discord.ext.Context)
                The context given by the discord bot.
            
            name : Optional[str]
                The name of the member we want to check points for.
            
            Returns
            _______
            **Returns** It will return the points of the corresponding 
            member.(string)
            If it fails, it will return a string with the error.
        """
        try:
            if(name == None):
                user = ctx.message.author
                return "You have {} points.".format(self.db.checkPoints(user))
            else:
                user = self.findName(ctx.message.server,name)
                return "{} has {} points".format(user.name,\
                    self.db.checkPoints(user))            
            
        except UserNotAdded as err:
            return err.message

        except UserInsufficentPermissions as err:
            return err.message 

        except InvalidType as err:
            print(err.message)
            return "An error occured... Sorry"

    def roll(self):
        """
            Rolls dice.

            Returns
            --------
            Returns a string if you won or lost.
            If error, returns the error string.
        """
        
        roll = self.games.rollDice()
        self.db.changeRollStats([roll]) 
        return "You rolled a {}".format(roll)

    def flipStats(self):
        """
            Returns a string with the flip stats.
            
            Returns
            --------
            **Returns** a string corresponding to the amount of heads and tails.
        """
        stats = self.db.flipstats
        return "Total Rolls: {}\nHeads: {}\nTails: {}".format(stats[2],\
            stats[0],stats[1])

    def rollStats(self):
        """
            Returns a string with the dice rolling stats.

            Returns
            -------
            **Returns** a string with corresponding roll information. 
        """ 
        stats = self.db.rollstats
        string = "Total Rolls: {}\n".format(stats[7])
        for i in range(1,6):
            string += "Number of {}s: {}\n".format(stats[i])
        string += "Number of {}s: {}".format(stats[6])

        return string

    def serverStats(self):
        """
            Returns a string with the server stats.
        
            Returns
            _______
            **Returns** a string with corresponding server information.
        """
        stats   = self.db.serverstats
        string  = "Total exchanged points: {}\nAmount of database accesses: {}"\
                .format(stats[0], stats[1])
        string += "\nBot Creation: {}\nAuthor: Garett Roberts".format(\
                stats[2])

        return string

    def givePoints(self,ctx,amount,to):
        """
            Gives the specified amount to the member

            Parameters
            ----------
            ctx    : (discord.ext.Context)
                A context given to us from the discord bot.

            amount : (int)
                The amount that we want to give.     

            to     : (str)
                The member we want to send the amount to. 

            Returns
            _______
            **Returns** a corresponding string showing success.
            If a failure, it will return the string of the error.
        """ 
        try:
            try:
                amount = int(amount)
            except:
                raise BadInput("Please make the amount a positive integer")

            if(amount < 0):
                raise BadInput("Please make the amount a positve integer")

            member = ctx.message.author
            opp    = self.findName(ctx.message.server,to)

            mpoints = self.db.checkPoints(member)
            if(mpoints - abs(amount) < 0):
                return "You do not have enough to give away {} points"\
                    .format(mpoints)
            
            self.db.exchangePoints(member,opp,amount)

            return "Gave {} points to {}".format(amount,opp.name)

        except UserNotAdded as err:
            return err.message
        except UserInsufficentPermissions as err:
            return err.message
        except BadInput as err:
            return err.message
        except InvalidType as err:
            print(err.message) 
            return "An error occured... Sorry"
