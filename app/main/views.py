from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from flask_login import login_required,current_user
from ..models import User,Pitch,Comment,Upvote,Downvote
from .forms import UpdateProfile,PitchForm
from .. import db,photos




# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Pitch Application'
    return render_template('index.html',title = title, Pitch = Pitch)


@main.route('/pitch/new')
@login_required
def new_pitch():
    form=PitchForm()
    if form.validate_on_submit():
        pitches=Pitch(category=form.category.data,content=form.content.data)
        db.session.add(pitches)
        db.session.commit()

        flash('pitch created')

        return redirect(url_for('main.new_pitch'))
    pitches=Pitch.query.all()
    return render_template('pitch.html',form=form, pitch=pitches)

        


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html",user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
