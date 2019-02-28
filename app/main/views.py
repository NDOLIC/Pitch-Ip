from flask import render_template,request,redirect,url_for, abort
from . import main

from .forms import UpdateProfile,CommentForm
from .. import db,photos
from ..models import Comment,Pitch,User
from flask_login import login_required, current_user
# import markdown2 
# from flask_fontawesome import FontAwesome


@main.route('/')
def index():
  title="Home| 60 seconds pitch"
  all_pitches = Pitch.get_pitches()
  
  return render_template('index.html',title=title, pitches = all_pitches)

@main.route('/pitch/new', methods = ['GET', 'POST'])
@login_required
def add_pitch():
    form = AddPitchForm()
    
    if form.validate_on_submit():
        category = form.category.data

        pitch = form.content.data

        new_pitch = Pitch(content=pitch, category = category, user=current_user)
        new_pitch.save_pitch()

        return redirect(url_for('main.index'))

    # all_pitches = Pitch.get_pitches()

    title = 'Add Pitch| 60 seconds pitch'    
    return render_template('pitches.html', title = title, pitch_form = form,user=current_user)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

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
        path = f'static/photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/new/comment/<int:id>', methods = ['GET','POST'])
@login_required
def add_comment(id):
  pitch=Pitch.query.filter_by(id=id).first()
  if pitch is None:
    abort(404)

  form=CommentForm()
  if form.validate_on_submit():
     comment=form.comment.data
     new_comment=Comment(content=comment ,pitch=pitch ,user=current_user)
     db.session.add(new_comment)  
     db.session.commit() 

     return redirect(url_for('main.index'))
  return render_template('comment.html', comment_form=form)

@main.route('/pitch/<int:id>')
def single_pitch(id):
    pitch=Pitch.query.filter_by(id=id).first()
    comments=Comment.get_comments(id=id)
    return render_template('pitch.html',pitch=pitch,comments=comments)

@main.route('/downvotes/<int:id>')
def upvoting(id):
    pitch1=Pitch.query.filter_by(id=id).first()
    pitch1.upvotes=Pitch.upvote(id)
    return redirect(url_for('main.single_pitch',pitch=pitch1.upvotes))

@main.route('/categories')
def categories():
    all_pitches = Pitch.get_pitches()
    path=[]
    for pitch in all_pitches:
        category=pitch.category
        path.append(category)
        return path

    return render_template('categories.html',category = path)