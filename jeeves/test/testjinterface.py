"""
    Filename: testjinterface.py
    Author:   Garett Roberts
    Repo:     https://github.com/garetroy/Jeeves
        
    This tests the JeevesUserInterface
"""

import sys,unittest
sys.path.insert(0, '../jeeves/')

from .                    import *
from datetime             import datetime, date, time
from discord              import Member, User, Server

class InterfaceTests(unittest.TestCase):
    
    def setUp(self):
        self.JUI        = JeevesUserInterface("God")
        self.JUI.db     = DB(self.JUI.hasPermission)

        self.dummydat = "2016-06-07 05:16:50.540000"
        self.user1    = {"username":"Gar","id":404,"discriminator":'dog',\
                        "avatar":"Nil"}
        self.user2    = {"username":"Frog","id":415,"discriminator":'dog',\
                        "avatar":"Nil"}
        self.user3    = {"username":"Blog","id":440,"discriminator":'dog',\
                        "avatar":"Nil"}
        self.member1  = Member(user=self.user1,roles=["Gods"],\
                        joined_at=self.dummydat)
        self.member2  = Member(user=self.user2,roles=["Gods"],\
                        joined_at=self.dummydat)
        self.member3  = Member(user=self.user3,roles=["Bad"],\
                        joined_at=self.dummydat)
        
        self.member2.nick = "Hoggar"

        self.usera = User(username="Flag",id=402,descriminator="glog",\
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
        with self.assertRaises(InvalidInput):
            self.JUI.hasPermissions(user1)

        with self.assertRaises(UserInsufficentPermissions):
            self.JUI.hasPermissions(member3)

        #Checks that there is nothing raised because they have permiss.
        self.JUI.hasPermissions(member2)
        self.JUI.hasPermissions(member1)

if __name__ == '__main__':
    unittest.main() 
