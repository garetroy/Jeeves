from random     import randrange
from discord    import Member,Role,utils
from .errors     import *
class Games:
    def __init__(self,debugnum=None):
        self.debugnum = debugnum
        self.numheads = 0
        self.numtails = 0

    def flipCoin(self):
        val =  randrange(0,2) if self.debugnum == None else self.debugnum
        if(val == 0):
            self.numheads += 1
            return 'heads'
        else:
            self.numtails += 1
            return 'tails'

    def flipCoinGuess(self,guess):
        side = self.flipCoin()

        if('s' not in guess.lower()): #head->heads, tail->tails
            guess += 's'

        if(guess.lower() not in ['heads','tails']):
            raise BadInput("Please use heads/tails")

        if(side == guess.lower()):
            return (True, "It was {}! You won.".format(side))
        return (False,"It was {}! You lost.".format(side))

    def neededAmount(self,numdice,bet):
        moniez      = numdice * bet
        probability = moniez*1000 if (1/6)**numdice < .007502 else moniez*5
        return probability

    def rollDiceBet(self,numdice,desirednum,bet):
        rolls      = [randrange(1,7) for i in range(numdice)]
        numcorrect = len([i for i in rolls if i == desirednum])
        numwrong   = numdice - numcorrect
       
        probility = (1/6)**numdice
        if(probility < .007502):
            return ((numcorrect*bet)*1000 - (numwrong*bet)*1000,rolls)
        else:
            return ((numcorrect*bet)*5 - (numwrong*bet)*5,rolls)
