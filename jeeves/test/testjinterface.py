"""
    Filename: testjinterface.py
    Author:   Garett Roberts
    Repo:     https://github.com/garetroy/Jeeves
        
    This tests the JeevesUserInterface
"""

import os, sys, unittest
sys.path.insert(0, os.path.abspath(".."))
from jeevesuserinterface import JeevesUserInterface as jui
from datetime            import datetime, date, time
from discord             import Member,User

class InterfaceTests(unittest.TestCase):
    
    def setUp(self):
        self.JUI      = jui()
        self.dummydat = "2016-06-07 05:16:50.540000"
        self.user1    = {"username":"Gar","id":404,"discriminator":'dog',\
                        "avatar":"Nil"}
        self.user2    = {"username":"Frog","id":415,"discriminator":'dog',\
                        "avatar":"Nil"}
        self.user3    = {"username":"Blog","id":440,"discriminator":'dog',\
                        "avatar":"Nil"}
        self.member1  = Member(user=self.user1,roles=["Gods"],\
                        joined_at=self.dummydat)
        self.member2  = Member(user=self.user2,roles=["Games"],\
                        joined_at=self.dummydat)
        self.member3  = Member(user=self.user3,roles=["Bad"],\
                        joined_at=self.dummydat)
        
        self.member2.nick = "Hoggar"

        self.usera = User(username="Flag",id=402,descriminator="glog",\
                     avatar="Nil")
        self.userb = User(username="Bag",id=1313,descriminator="glog",\
                     avatar="Nil")
        self.userc = User(username="Sag",id=9,descriminator="glog",\
                     avatar="Nil")

    def test_creation(self):
        self.assertIsInstance(self.JUI,jui)
        self.assertEqual(self.JUI.numheads, 0)
        self.assertEqual(self.JUI.numtails, 0)
        self.assertEqual(self.JUI.usersTable, {})

    def test_cssify(self):
        string  = "```css\nTestingme```"
        string2 = "```css\nTesting Me```"
        string3 = "```css\n31 asdf 1 ```"
        self.assertEqual(self.JUI.cssify("Testingme") ,string)
        self.assertEqual(self.JUI.cssify("Testing Me"),string2)
        self.assertEqual(self.JUI.cssify("31 asdf 1 "),string3)

    def test_hasPermissions(self):
        with self.assertRaises(ValueError) as cm:
            self.JUI.hasPermission(self.userb) 

        self.assertTrue(self.JUI.hasPermission(self.member1))
        self.assertTrue(self.JUI.hasPermission(self.member2))
        self.assertFalse(self.JUI.hasPermission(self.member3))

    def test_addUser(self):
        self.assertTrue(self.JUI.addUser(self.member1))
        self.assertTrue(self.JUI.addUser(self.member2))
        self.assertFalse(self.JUI.addUser(self.member3))
        
        with self.assertRaises(ValueError) as cm:
            self.JUI.addUser(self.usera)

        with self.assertRaises(KeyError) as cm:
            self.JUI.usersTable[self.usera] #Making sure they're not in there

    def test_checkPoints(self):
        self.assertEqual(self.JUI.checkPoints(self.member1),0)
        self.assertEqual(self.JUI.checkPoints(self.member2),0)
        
        with self.assertRaises(ValueError) as cm:
            self.JUI.checkPoints(self.userb)

        with self.assertRaises(KeyError) as cm:
            self.JUI.checkPoints(self.member3)

        with self.assertRaises(KeyError) as cm:
            self.JUI.usersTable[self.member3].points += 3 

        self.JUI.usersTable[self.member2].points = 5
        self.assertEqual(self.JUI.checkPoints(self.member2),5)

    def test_exchangePoints(self):
        with self.assertRaises(ValueError) as cm:
            self.JUI.exchangePoints(self.member1,self.usera,4)

        with self.assertRaises(KeyError) as cm:
            self.JUI.exchangePoints(self.member3,self.member1,4)

        self.JUI.exchangePoints(self.member2,self.member1,5)
        self.assertEqual(self.JUI.checkPoints(self.member1),5)
        self.assertEqual(self.JUI.checkPoints(self.member2),-5)
         

        self.JUI.exchangePoints(self.member1,self.member2,10099292292929290022)
        self.assertEqual(self.JUI.checkPoints(self.member1),-sys.maxsize)
        self.assertEqual(self.JUI.checkPoints(self.member2),sys.maxsize)
      
    def test_flipCoin(self):
        self.JUI.debugnum = 1 
        self.assertEqual(self.JUI.flipCoin(),'tails')
        self.JUI.debugnum = 0
        self.assertEqual(self.JUI.flipCoin(),'heads')
        
        self.assertEqual(self.JUI.numheads,1)
        self.assertEqual(self.JUI.numtails,1)

    def test_flipCoinGuess(self):
        self.JUI.debugnum = 1
        winstring         = "It was {}! You won."
        losestring        = "It was {}! You lost."
        curresult         = (True,winstring.format('tails'))
        self.assertEqual(self.JUI.flipCoinGuess('TaIlS'),curresult)

        curresult         = (False,losestring.format('tails'))
        self.assertEqual(self.JUI.flipCoinGuess('HeAds'),curresult)

        self.JUI.debugnum = 0
        curresult         = (False,losestring.format('heads'))
        self.assertEqual(self.JUI.flipCoinGuess('TaIlS'),curresult)

        curresult         = (True,winstring.format('heads'))
        self.assertEqual(self.JUI.flipCoinGuess('HeAds'),curresult)

    def test_filpCoinBest(self):
        with self.assertRaises(ValueError) as cm:
            self.JUI.flipCoinBet(self.usera,self.member1,'heads', 1)  

        with self.assertRaises(ValueError) as cm:
            self.JUI.flipCoinBet(self.member2,self.userc,'heads', 22)  

        expectedstring = "Sorry, you don't have permissions to bet"
        self.assertEqual(self.JUI.flipCoinBet(self.member3,self.member2,\
            'heads',12), expectedstring)

        expectedstring = "Sorry you or the opponent does not have sufficent funds."
        self.assertEqual(self.JUI.flipCoinBet(self.member2,self.member1,\
            'tails',1555),expectedstring)

        self.JUI.debugnum = 0
        self.JUI.flipCoinBet(self.member1,self.member3,'tails',1415)

        self.assertEqual(self.JUI.checkPoints(self.member1),-1415)
        self.assertEqual(self.JUI.checkPoints(self.member3),1415)

        self.JUI.debugnum = 1
        self.JUI.flipCoinBet(self.member1,self.member2,'tails',1415)
        self.assertEqual(self.JUI.checkPoints(self.member1),0)
        self.assertEqual(self.JUI.checkPoints(self.member2),-1415)

if __name__ == '__main__':
    unittest.main() 
