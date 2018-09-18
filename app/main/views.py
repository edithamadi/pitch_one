from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from flask_login import login_required,current_user
from ..models import User,Pitch,Comment
from .forms import UpdateProfile,PitchForm,CommentForm
from .. import db,photos
# import markdown2

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Pitch Application'
    pitch = Pitch.query.all()
    # categories = Category.get_categories()
    return render_template('index.html',title = title, Pitch = pitch)

@main.route('/pitch/new', methods=['GET','POST'])
@login_required
def new_pitch():
    form=PitchForm()
    if form.validate_on_submit():
        pitches=Pitch(category=form.category.data,pitch_content=form.content.data)
        db.session.add(pitches)
        db.session.commit()

        flash('pitch created')

    pitches=Pitch.query.all()
    return render_template('pitch.html',form=form, pitch=pitches)

,1,00


@main.route('/category/<int:id>')
def category(id):

    category = PitchCategory.query.get(id)
    category_name = PitchCategory.query.get(category_name)

    if category is None:
        abort(404)

    pitch_in_category = Pitch.get_pitch(id)
    return render_template('category.html' ,category= category, pitch= pitch_in_category)


@main.route('/pitch/comments/new/<int:id>',methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(pitch_id =id,data=form.comment.data)
        new_comment.save_comment()
        return redirect(url_for('main.new_pitch'))
    return render_template('ncomment.html', form=form)

@main.route('/comments/<int:id>')
def single_comment(id):
    comment=Comment.query.get(id)
    if comment is None:
        abort(404)
    return render_template('new_comment.html')

@main.route('/view/comment/<int:id>')
def view_comments(id):
    '''
    Function that shows the comments of a particular pitch
    '''
    comments = Comment.get_comments(id)
    
    return render_template('viewcomment.html',comments = comments, id=id)

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