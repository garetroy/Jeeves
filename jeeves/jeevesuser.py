from discord import User as Us
class JeevesUser:
    def __init__(self,userinstance):
        if not isinstance(userinstance,Us):
            raise ValueError
    
        self.id         = userinstance.id
        self.name       = userinstance.name
        self.points     = 100 
        self.leaugename = None
        self.leaugeid   = None 
        self.runescapen = None #runescapename
        self.remindlive = [] #(leaugeid,True/False)
        self.remindlupd = False #Message if new leauge patch
        self.callme     = (None,None) #(nickname, True/False)  

    def __eq__(self,other):
        if not isinstance(other,JeevesUser):
            raise ValueError
        
        return other.id == self.id

    def __ne__(self,other):
        return not self == other

    def __gt__(self,other):
        if not isinstance(other,JeevesUser):
            raise ValueError
        
        return self.points > other.points

    def __lt__(self,other):
        return not self > other

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<JeevesUser (id={}, name={}, points={})>".format(\
                self.id, self.name, self.points)
   
        
