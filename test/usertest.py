import os, sys, unittest
sys.path.insert(0, os.path.abspath(".."))
from jeevesuser import JeevesUser as Ju
from discord    import User as Us

class UserTests(unittest.TestCase):

    def test_discordUserCreation(self):
        u = Us(username="dog", id="3", discriminator="k",\
            avatar=None,bot=True)

        self.assertIsInstance(u,Us)
        self.assertEqual(u.name,"dog")
        self.assertEqual(u.id,"3")
        self.assertEqual(u.discriminator,"k")

    def test_jeevesUserCreation(self):
        u = Us(username="dog", id="3", discriminator="k",\
            avatar=None,bot=True)

        ju = Ju(u)
        self.assertIsInstance(ju,Ju)
        self.assertEqual(ju.name,"dog")
        self.assertEqual(ju.id,"3")

    def test_jeevesUsersInteraction(self):
        u = Us(username="dog", id="3", discriminator="k",\
            avatar=None,bot=True)

        ju  = Ju(u)
        ju2 = Ju(u)
        ju.points  = 10
        ju2.points = 20
        
        self.assertEqual(ju,ju2)
        self.assertTrue(ju < ju2)
        self.assertFalse(ju > ju2)
        

if __name__ == '__main__':
    unittest.main()
