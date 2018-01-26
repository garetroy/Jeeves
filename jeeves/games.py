from random     import randrange
from discord    import Member,Role,utils
from .errors     import *
class Games:
    """
        A game class with different games.
        
        Parameters
        -----------
        debugnum = Optional[int=None]
            This is for debugging purposes.
    """
    def __init__(self,debugnum=None):
        self.debugnum = debugnum
        self.numheads = 0
        self.numtails = 0

    def flipCoin(self):
        """
            Flips a coin.
            
            Returns
            --------
            **Returns** string ('heads'/'tails')
        """
        val =  randrange(0,2) if self.debugnum == None else self.debugnum
        if(val == 0):
            return 'heads'
        else:
            return 'tails'

    def flipCoinGuess(self,guess):
        """
            Flips a coin, and compares it against a guess
            
            Parameters
            -----------
            guess : (str)
                A string indicating the guess ('heads'/'tails') 

            Raises
            -------
            BadInput
                This is if the guess is not correctly formatted.

            Returns
            -------
            **Returns** A tuple (bool,str,str), the bool indicating winning or
            losing. The first string to generate a win/lose message. The last
            string with what the result was.
        """
        side = self.flipCoin()

        if('s' not in guess.lower()): #head->heads, tail->tails
            guess += 's'

        if(guess.lower() not in ['heads','tails']):
            raise BadInput("Please use heads/tails")

        if(side == guess.lower()):
            return (True, "It was {}! You won.".format(side),side)
        return (False,"It was {}! You lost.".format(side),side)

    def rollDice(self):
        """
            Rolls a dice.

            Returns
            --------
            **Returns** An int between 1 and 6.
        """
        return randrange(1,7)
