
# from flask import render_template,redirect,url_for,abort,request
# from . import main
# from flask_login import login_required,current_user
# from ..models import User,Comment,Pitch
# from .forms import UpdateProfile,CommentForm,PitchForm
# from .. import db,photos



# @main.route('/')
# def index():

#     '''
#     View root page function that returns the index page and its data
#     '''

#     message = 'Hello World'
#     return render_template('index.html',message = message)


# @main.route('/movie/<int:id>')
# def movie(id):

#     '''
#     View movie page function that returns the movie details page and its data
#     '''
#     movie = get_movie(id)
#     title = f'{movie.title}'
#     reviews = Review.get_reviews(movie.id)

#     return render_template('movie.html',title = title,movie = movie,reviews = reviews)



# @main.route('/user/<uname>')
# def profile(uname):
#     user = User.query.filter_by(username = uname).first()

#     if user is None:
#         abort(404)

#     return render_template("profile/profile.html", user = user)



# @main.route('/user/<uname>/update',methods = ['GET','POST'])
# @login_required
# def update_profile(uname):
#     user = User.query.filter_by(username = uname).first()
#     if user is None:
#         abort(404)

#     form = UpdateProfile()

#     if form.validate_on_submit():
#         user.bio = form.bio.data

#         db.session.add(user)
#         db.session.commit()

#         return redirect(url_for('.profile',uname=user.username))

#     return render_template('profile/update.html',form =form)


# @main.route('/user/<uname>/update/pic',methods= ['POST'])
# @login_required
# def update_pic(uname):
#     user = User.query.filter_by(username = uname).first()
#     if 'photo' in request.files:
#         filename = photos.save(request.files['photo'])
#         path = f'photos/{filename}'
#         user.profile_pic_path = path
#         db.session.commit()
#     return redirect(url_for('main.profile',uname=uname))
from flask import render_template, request, redirect, url_for, abort
from . import main
from .forms import PitchForm, CommentForm, Vote  
from ..models import User, Pitch, Comment
from flask_login import login_required, current_user
from .. import db, photos



@main.route('/')
def index():
    """
    Function that renders the index.html and its content
    """
    pitches = Pitch.query.all()

    return render_template('index.html', pitches=pitches)


@main.route('/business')
def business():
    """
    Function that renders the business category pitches and its content
    """
    business_pitch = Pitch.query.filter_by(category='business').all()

    return render_template('business.html', business=business_pitch)


@main.route('/jobs')
def jobs():
    """
    Function that renders the job category pitches and its content
    """

    jobs_pitch = Pitch.query.filter_by(category='jobs').all()

    return render_template('jobs.html', jobs=jobs_pitch)


@main.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    pitch_form = PitchForm()

    if pitch_form.validate_on_submit():
        title = pitch_form.title.data
        body = pitch_form.body.data
        author = pitch_form.author.data
        category = pitch_form.category.data
        # category=category
        new_pitch = Pitch(title=title, body=body,
                          author=author, category=category, upvotes=0,
                          downvotes=0,
                          users=current_user)
        new_pitch.save_pitches()
        return redirect(url_for('main.index'))

    return render_template('new.html', pitch_form=pitch_form)


@main.route('/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    comment_form = CommentForm()
    vote_radio = Vote()
    pitch = Pitch.query.get(id)
    if comment_form.validate_on_submit():
        title = comment_form.title.data
        comment = comment_form.comment.data
        # category=category
        new_comment = Comment(comment=comment,
                              title=title,
                              user=current_user)
        new_comment.save_comment()
        return redirect(url_for('main.index'))

    return render_template('comment.html',
                           comment_form=comment_form,
                           pitch=pitch,
                           vote_radio=vote_radio)


@main.route('/update', methods=['POST'])
def update():
    pitch = Pitch.query.get(id)
    pitch.upvotes = request.args.get('jsdata')
    pitch.downvotes = request.args.get('jsdata')

    return render_template('button.html', pitch=pitch)


@main.route('/user/<uname>')
@login_required
def profile(uname):
    """
    Function that renders the profile page of our user
    """
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)

@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))