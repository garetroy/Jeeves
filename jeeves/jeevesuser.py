from discord                    import Member
from sqlalchemy                 import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JeevesUser(Base):
    __tablename__ = 'JeevesUser'

    id         = Column(Integer, primary_key=True)
    discordid  = Column(String)
    name       = Column(String)
    points     = Column(Integer)
    leaugename = Column(String)
    runescapen = Column(String)
    remindupd  = Column(Boolean)
    
    def __init__(self,userinstance):
        if not isinstance(userinstance,Member):
            raise InvalidType(type(userinstance),type(Member),"JeevesU init")
    
        self.discordid  = userinstance.id
        self.name       = userinstance.name
        self.points     = 100 
        self.leaugename = None
        self.leaugeid   = None 
        self.runescapen = None #runescapename
        self.remindlupd = False #Message if new leauge patch

    def __eq__(self,other):
        if(other == None):
            return False
        if not isinstance(other,JeevesUser):
            raise InvalidType(type(other),type(JeevesUser), "JU eq") 
        
        return other.id == self.id

    def __ne__(self,other):
        return not self == other

    def __gt__(self,other):
        if not isinstance(other,JeevesUser):
            raise InvalidType(type(other),type(JeevesUser), "JU gt")
        
        return self.points > other.points

    def __lt__(self,other):
        return not self > other

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<JeevesUser (id={}, name={}, points={})>".format(\
                self.id, self.name, self.points)
   
        
