from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker
from discord        import Member
from .jeevesuser    import JeevesUser,Base
from .errors        import *

class DB:
    def __init__(self,checkpermmethod):
        self.engine    = create_engine('sqlite:///jeeves.db',echo=True) 
        Base.metadata.create_all(self.engine)
        self.Session   = sessionmaker(bind=self.engine)
        self.session   = self.Session()
        self.checkperm = checkpermmethod
        
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

    def getUser(self,member,addUser=False):
        if isinstance(member,Member):
            memberid = member.id

        print(member.id)
        print(addUser)

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
