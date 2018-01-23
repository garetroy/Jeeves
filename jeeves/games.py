from random     import randrange
from discord    import Member,Role,utils
from errors     import *
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
