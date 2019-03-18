from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

class User(UserMixin,db.Model):
    __tablename__='users'

    id = db.Column(db.Integer,primary_key=True)
    username= db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True , index=True)
    bio= db.Column(db.String(255))
    profile_pic_path = db.Column(db.String(255))
    pass_secure=db.Column(db.String(255))
    pitches= db.relationship('Pitch',backref='user', lazy='dynamic')
    comments = db.relationship('Comment',backref='user' ,lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Pitch(db.Model):
   __tablename__ = 'pitches'

   id = db.Column(db.Integer,primary_key = True)
   user_id= db.Column(db.Integer,db.ForeignKey('users.id'))
   content = db.Column(db.String(255))
   comments = db.relationship('Comment',backref='pitch' ,lazy='dynamic')
   category = db.Column(db.String(255))
   upvotes = db.Column(db.Integer)
   downvotes = db.Column(db.Integer)


   def save_pitch(self):
        db.session.add(self)
        db.session.commit()

   @classmethod
   def clear_pitches(cls):
        Pitch.all_pitches.clear()

   @classmethod
   def get_pitche(cls,id):
        pitche = Pitch.query.filter_by(user_id=id).all()
        return pitche
    
   @classmethod
   def get_pitches(cls):
       pitches = Pitch.query.filter_by().all()
       return pitches

   @classmethod
   def upvote(cls,id):
       pitch=Pitch.query.filter_by(pitch_id=id).all()
       upvotes=0
       upvotes=pitch.upvotes+1
       return upvote

   @classmethod
   def downvote(cls,id):
       pitch=Pitch.query.filter_by(pitch_id=id).all()
       downvotes=0
       downvotes=pitch.downvotes+0
       return downvote

#    class Vote(Model):
#     user_id = IntegerField(null=True)
#     post_id = IntegerField(null=True)

#     class Meta:
#         database = DATABASE




class Comment(db.Model):
    __tablename__= 'comments'
    
    id= db.Column(db.Integer,primary_key= True)
    content = db.Column(db.String(255))
    user_id= db.Column(db.Integer,db.ForeignKey('users.id'))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))


    def save_comment(self):
        '''
        save the comment per post
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_comments(cls):
        Comment.all_comments.clear()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(pitch_id=id).all()
        return comments

    @classmethod
    def get_commentss(cls,id):
        comments = Comment.query.filter_by(user_id=id).all()
        return comments

    class PhotoProfile(db.Model):
        __tablename__ = 'profile_photos'

        id = db.Column(db.Integer,primary_key = True)
        pic_path = db.Column(db.String())
        user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

