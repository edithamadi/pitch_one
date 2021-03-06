from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(UserMixin,db.Model): # we pass in db.model to allow 
                                # connect our class and database to allow communication 
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))

    pitches = db.relationship('Pitch', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref = 'user', lazy = 'dynamic')
    

    @property
    def password(self):
         raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self): # _repr_ method makes it easier to debug our application
        return f'{self.username}'

class Pitch(db.Model):
    __tablename__ = 'pitch'

    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    category = db.Column(db.String(255))
    pitch_content = db.Column(db.String(255))
    
    comments = db.relationship('Comment', backref = 'pitch', lazy = 'dynamic')

    def __repr__(self):
        return f'Pitch {self.pitch_content}'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    data = db.Column(db.String(255))
    

    def __repr__(self):
        return f'Comment {self.data}'
    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self, id):
        comment = Comment.query.filter_by(pitch_id=id).all()
        return comment