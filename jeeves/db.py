from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker
from discord        import Member
from .jeevesuser    import JeevesUser,Base
from .errors        import *

class DB:
    """
        Represents a sqllite database, that uses sqlalchemy to 
        store, retrieve, and delete data.

        .. _discord.Member: https://discordpy.readthedocs.io/en/latest/api.html#discord.Member

    :class: `JeevesUserInterface` takes one argument.

    Parameters
    ----------
    checkpermmethod : (function)
        This method is what we will check permissions with.

    Attributes
    -----------
    engine : sqlalchemy engine
        The engine for sqlalchemy.

    session : sqlalchemy session
        The session for the database.

    hasPermisssion : function
        The function for checking permissions.
    """
    def __init__(self,checkpermmethod):
        self.engine        = create_engine('sqlite:///jeeves.db',echo=True) 
        Base.metadata.create_all(self.engine)
        self.Session       = sessionmaker(bind=self.engine)
        self.session       = self.Session()
        self.hasPermission = checkpermmethod
        
    def addUser(self,member,cmdfrom=None):
        """
            Adds user to the hashtable. This will be replaced by a 
            database in the near future.

            Parameters
            ----------
            member  : (`discord.Member`_)
                The member that we want to add.

            cmdfrom : Optional[`discord.Member`_]
                If populated, checks the permissions of this member
                to see if we can add the member to the group.

            Raises
            -------
           InvalidType 
                member or cmndfrom was not `discord.Member`_ instance.

            UserInsufficentPermissions
                This will be indirectly raised from `hasPermission`.

            Returns
            --------
            **Returns** `JeevesUser` instance.
        """
        if not isinstance(member, Member):
            raise InvalidType(type(member),type(Member),"DB.addUser1")

        if(cmdfrom != None and not isinstance(cmdfrom, Member)):
            raise InvalidType(type(member),type(Member),"DB.addUser2")

        #checks permissions for member, if cmdfrom declared
        #then it checks if cmdfrom has permissions to add the member instead
        #self.checkperm(member if cmdfrom == None else cmdfrom)

        memberres = self.getUser(member,addUser=True)
        if memberres != None:
            return memberres 
        
        if isinstance(member,Member):
            member = JeevesUser(member)

        elif not isinstance(member,JeevesUser):
            raise InvalidType(type(member), type(JeevesUser), "DB.addUser3")

        self.session.add(member)
        self.session.commit()
        return member

    def deleteUser(self,member):
        """
            Finds member in the database then deletes them.

            Parameters
            -----------
            member : `discord.Member`_
                The member we wnat to delete.

            Raises
            ______
            UserNotAdded
                When the member dosen't exist in the database.
        """
        self.session.delete(self.getMember) 
        self.session.commit()

    def getUser(self,member,addUser=False):
        """
            Get's the User entry from the corresponding member.

            Parameters
            ----------
            member : (`discord.Member`_)
                The member we want to look up
            
            addUser : Optional[addUser=False]
                This will bypass raising user not added

            Raises
            -------
            UserNotAdded
                If it can't find the user.

            Returns
            --------
            **Returns** Member if found.
            Returns None if adduser is True       
        """
        if isinstance(member,Member):
            memberid = member.id


        user = self.session.query(JeevesUser).\
            filter_by(discordid=memberid).first()

        if(user == None and not addUser):
            raise UserNotAdded(member.name)

        return user

    def checkPoints(self, member):
        """
            Returns the points from a given member.

            Parameters
            ----------
            member : (`discord.Member`_)
            
            Raises
            -------
           InvalidType 
                The member was not a `discord.Member`_ instance.
            
            Returns
            -------
            **Returns** the correspoing points. (int) 
            
        """
        if not isinstance(member, Member):
            raise InvalidType(type(member),type(Member),"DB.checkPoints")

        return self.addUser(member).points

    def exchangePoints(self, member1, member2, amount):
        """
            Subtracts the amount from one user and gives it to another.
        
            Parameters
            ----------
            member1 : (`discord.Member`_)
                The member we are taking the amount from.

            member2 : (`discord.Member`_)
                The member we are giving the amount to.

            amount  : (int)
                The amount we are exchanging.

            Raises
            -------
            See raises from `addUser`
        """ 
        if not isinstance(member1, Member):
            raise InvalidType(type(member),type(Member),"DB.exchangePoints1")
        if not isinstance(member2, Member):
            raise InvalidType(type(member),type(Member),"DB.exchangePoints2")

        member1 = self.addUser(member1) 
        member2 = self.addUser(member2)
        member1.points -= amount
        member2.points += amount
        self.session.commit()
