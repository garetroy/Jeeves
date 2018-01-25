from discord                    import Member
from sqlalchemy                 import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JeevesUser(Base):
    """
        A JeevesUser class that is also a sqlalchmey base.
        (This means it is OMR, automatically generated tables from
        the class definition)

        .. _discord.Member: https://discordpy.readthedocs.io/en/latest/api.html#discord.Member

        Parameters
        -----------
        memberinstance : `discord.Member`_
            The instance of the Member that we want to conver to JeevesUser.
        
        Attributes
        -----------
        discordid : string
            A string representing the discord id.
        
        name : string
            The name of the member.
        
        points : int
            The amount of points the member has.

        leaugename : string
            The leauge name of the individual.

        runescapen : string
            The runescape name of the member.

        remindupd : bool
            A boolean indicating if the member wants to be remined of updates.
    """
    __tablename__ = 'JeevesUser'

    id         = Column(Integer, primary_key=True)
    discordid  = Column(String)
    name       = Column(String)
    points     = Column(Integer)
    leaugename = Column(String)
    runescapen = Column(String)
    remindupd  = Column(Boolean)
    
    def __init__(self,memberinstance):
        if not isinstance(memberinstance,Member):
            raise InvalidType(type(memberinstance),type(Member),"JeevesU init")
    
        self.discordid  = memberinstance.id
        self.name       = memberinstance.name
        self.points     = 100 
        self.leaugename = None
        self.leaugeid   = None 
        self.runescapen = None #runescapename
        self.remindlupd = False #Message if new leauge patch

    def __eq__(self,other):
        """
            An equal method.

            Raises
            -------
            InvalidType
                If it is not a corresponding type.
        """
        if(other == None):
            return False
        if not isinstance(other,JeevesUser):
            raise InvalidType(type(other),type(JeevesUser), "JU eq") 
        
        return other.id == self.id

    def __ne__(self,other):
        """
            An not equal method.

            Raises
            -------
            InvalidType
                If it is not a corresponding type.
        """
        return not self == other

    def __gt__(self,other):
        """
            An greaterthan method.

            Raises
            -------
            InvalidType
                If it is not a corresponding type.
        """
        rif not isinstance(other,JeevesUser):
            raise InvalidType(type(other),type(JeevesUser), "JU gt")
        
        return self.points > other.points

    def __lt__(self,other):
        """
            An lessthan method.

            Raises
            -------
            InvalidType
                If it is not a corresponding type.
        """
        r
        return not self > other

    def __str__(self): 
        """
            A string method.
        """
        return self.name

    def __repr__(self):
        """
            A represent method.
        """
        return "<JeevesUser (id={}, name={}, points={})>".format(\
                self.id, self.name, self.points)
   
        
