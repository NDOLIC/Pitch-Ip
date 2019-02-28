import unittest
from app.models import Movie

# class MovieTest(unittest.TestCase):
#     '''
#     Test Class to test the behaviour of the Movie class
#     '''

#     def setUp(self):
#         '''
#         Set up method that will run before every Test
#         '''
#         self.new_movie = Movie(1234,'Python Must Be Crazy','A thrilling new Python Series','/khsjha27hbs',8.5,129993)

#     def test_instance(self):
#         self.assertTrue(isinstance(self.new_movie,Movie))

# if __name__ == '__main__':
#     unittest.main()
import unittest
from app.models import Pitch, User
# from flask_login import current_user
# from app import db


class TestPitch(unittest.TestCase):

    def setUp(self):
        self.user = User(
            username='', password='', email='')
        self.new_pitch = Pitch(title='',body="",author='',category='',upvotes=,downvotes=,user=self.user)

    def tearDown(self):
        Pitch.query.delete()
        User.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch, Pitch))

    def test_check_instance_variables(self):
        self.assertEquals(
            self.new_pitch.title, 'Elevator Pitch Example for an Professional Accountant')
        self.assertEquals(self.new_pitch.body, "Test Pitch")
        self.assertEquals(self.new_pitch.author,
                          'Improv Andy')
        self.assertEquals(self.new_pitch.category,
                          'business')
        self.assertEquals(self.new_pitch.upvotes,
                          1)
        self.assertEquals(self.new_pitch.downvotes,
                          0)
        self.assertEquals(self.new_pitch.user, self.user_James)

    def test_save_pitch(self):
        self.new_pitch.save_pitches()
        self.assertTrue(len(Pitch.query.all()) > 0)