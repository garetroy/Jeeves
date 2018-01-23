import os, sys, unittest
sys.path.insert(0, os.path.abspath(".."))
from games   import Games
from errors   import *
from discord  import Member
from datetime import datetime, date, time

class GamesTests(unittest.TestCase):

    def setUp(self):
        self.games = Games()
        self.user1    = {"username":"Gar","id":404,"discriminator":'dog',\
                        "avatar":"Nil"}
        self.dummydat = "2016-06-07 05:16:50.540000"
        self.member1  = Member(user=self.user1,roles=["Gods"],\
                        joined_at=self.dummydat)
 
    def test_flipCoin(self):
        self.games.debugnum = 1 
        self.assertEqual(self.games.flipCoin(),'tails')
        self.games.debugnum = 0
        self.assertEqual(self.games.flipCoin(),'heads')
        
        self.assertEqual(self.games.numheads,1)
        self.assertEqual(self.games.numtails,1)

    def test_flipCoinGuess(self):
        self.games.debugnum = 1
        winstring         = "It was {}! You won."
        losestring        = "It was {}! You lost."
        curresult         = (True,winstring.format('tails'))
        self.assertEqual(self.games.flipCoinGuess('TaIlS'),curresult)

        curresult         = (False,losestring.format('tails'))
        self.assertEqual(self.games.flipCoinGuess('HeAds'),curresult)

        self.games.debugnum = 0
        curresult         = (False,losestring.format('heads'))
        self.assertEqual(self.games.flipCoinGuess('TaIlS'),curresult)

        curresult         = (True,winstring.format('heads'))
        self.assertEqual(self.games.flipCoinGuess('HeAds'),curresult)

        with self.assertRaises(BadInput):
            self.games.flipCoinGuess('dog')

        with self.assertRaises(BadInput):
            self.games.flipCoinGuess('hea')

        with self.assertRaises(BadInput):
            self.games.flipCoinGuess('tais')

if __name__ == '__main__':
    unittest.main() 
