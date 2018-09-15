from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,ValidationError
from wtforms.validators import Required,Email
from ..models import User,Pitch,Comment,Upvote,Downvote

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):
   category = StringField('Category', validators=[Required()])
   content= TextAreaField('Content', validators=[Required()])
   submit = SubmitField('sumbit')

