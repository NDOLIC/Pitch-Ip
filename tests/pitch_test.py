import unittest
from app.models import Pitch,User
from app import db



class PitchModelTest(unittest.TestCase):
   def setUp(self):
        self.user_James = User(username = 'claire',password = 'food', email = 'tblaguese1@gmail.com', bio='Good',profile_pic_path='https://sss.com')
        self.new_pitch = Pitch(id=1234,content='Pitch ',category="hhh",upvotes=12,downvotes=34,user = self.user_James )

   def tearDown(self):
        User.query.delete()
        Pitch.query.delete()


   def test_check_instance_variables(self):
        self.assertEquals(self.new_pitch.id,1234)
        self.assertEquals(self.new_pitch.content,'Pitch ')
        self.assertEquals(self.new_pitch.category,"hhh")
        self.assertEquals(self.new_pitch.upvotes,2)
        self.assertEquals(self.new_pitch.downvotes,4)
        self.assertEquals(self.new_pitch.user,self.user_James)

   def test_save_pitch(self):
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitch.query.all())>0)  

   def test_get_pitch_by_id(self):

        self.new_pitch.save_pitch()
        got_pitchs = Pitch.get_pitche(1234)
        self.assertTrue(len(got_pitchs) == 1)    

if __name__ == '__main__':
    unittest.main()