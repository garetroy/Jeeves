from sqlalchemy                      import Column, Integer, String, Boolean
from sqlalchemy                      import DateTime, ForeignKey
from sqlalchemy.orm                  import relationship, backref
from sqlalchemy.ext.declarative      import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy 
from datetime                        import datetime

Base = declarative_base()

class JeeveStats(Base):
    """
        This class is the stats class contining stats on all things
        Jeeves.

    """

    __tablename__   = "JeeveStats"
    id              = Column(Integer, primary_key=True)
    exchangedpoints = Column(Integer) 
    databaseaccess  = Column(Integer)
    creationdate    = Column(DateTime)
    gamestatsrel    = relationship("GameStats", backref=\
            backref("JeeveStats", uselist=False)) 
    gamestats       = association_proxy('gamestatsrel','GameStats')
    
    def __init__(self):
        self.exchangedpoints = 0
        self.databaseaccess  = 1 #includes commits and queries
        self.creationdate    = datetime.now()

class GameStats(Base):
    """
        Contains the  stats of a dice roll.
    """

    __tablename__ = "GameStats"
    id            = Column(Integer, primary_key=True)
    jeevestatsid  = Column(Integer, ForeignKey('JeeveStats.id'))
    numheads      = Column(Integer)
    numtails      = Column(Integer)
    numflips      = Column(Integer)
    numrolls      = Column(Integer)
    numones       = Column(Integer)
    numtwos       = Column(Integer)
    numthrees     = Column(Integer)
    numfours      = Column(Integer)
    numfives      = Column(Integer)
    numsixes      = Column(Integer)

    def __init__(self):
        self.numrolls      = 0
        self.numones       = 0
        self.numtwos       = 0
        self.numthrees     = 0
        self.numfours      = 0
        self.numfives      = 0
        self.numsixes      = 0
        self.numheads      = 0
        self.numtails      = 0
        self.numflips      = 0
    
