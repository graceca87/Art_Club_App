from tkinter import Image
from app import app, db
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm, ImageForm, CommentForm
from app.models import User, Piece, Comment
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import cloudinary
import os
import cloudinary.uploader
import cloudinary.api


load_dotenv()

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    # if the form is submitted and all the data is valid
    if form.validate_on_submit():
        print('Form has been validated! Hooray!!!!')
        email = form.email.data
        username = form.username.data
        password = form.password.data
        # Before we add the user to the database, check to see if there is already a user with username or email
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash('A user with that username or email already exists.', 'danger')
            return redirect(url_for('signup'))
        new_user = User(email=email, username=username, password=password)
        flash(f"{new_user.username} has been created.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['Get', 'Post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #get username and pw from form
        username = form.username.data
        password = form.password.data
        # Query user table for a user with the same username as the form
        user = User.query.filter_by(username=username).first()
        # if user exists and password is correct for that user
        if user is not None and user.check_password(password):
            # Log the user in with the login_user function from flask_login
            login_user(user)
            # Redirect back to the home pageUnboundLocalError: local variable 'user' referenced before assignment
            flash(f"welcome back, {user.username}!", "success")
            return redirect(url_for('gallery'))
        # If no user with username or password incorrect
        else:
            # flash a danger message
            flash('Incorrect username and/or password. Please try again', 'danger') 
            # Redirect back to login
            return redirect(url_for('gallery'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out.', 'primary')
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/critique-room', methods=['GET', 'POST'])
def critique_room():
    form=ImageForm()
    return render_template('critique_room.html', form=form)


@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    pieces = Piece.query.order_by(Piece.date_created.desc())
    form = CommentForm()
    if form.validate_on_submit():
        comments = form.comments.data
        piece_id = form.piece_id.data
        comment = Comment(text=comments, piece_id=piece_id, user_id=current_user.id)
        return redirect(url_for('gallery'))
    comments = Comment.query.order_by(Comment.timestamp.asc())
    return render_template('gallery.html', pieces=pieces, form=form, comments=comments)

# @app.route('/portfolio')
# def portfolio():
#     pieces = current_user.pieces
#     return render_template('portfolio.html', user=current_user, pieces=pieces)


@app.route('/pieces/<piece_id>/view')
def view_piece(piece_id):
    piece = Piece.query.get_or_404(piece_id)
    return render_template('view_piece.html', piece=piece)


@app.route('/portfolio/<user_id>')
def artist_portfolio(user_id):
    user = User.query.get_or_404(user_id)
    pieces = user.pieces
    return render_template('portfolio.html', user=user, pieces=pieces)
 



@app.route("/upload-art", methods=['GET', 'POST'])
def upload_file():
    form=ImageForm()
    # ------------------- fetching images from cloudinary ------------------
    app.logger.info('in upload route')
    if request.method == 'POST' and form.validate_on_submit():
        cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
        api_secret=os.getenv('API_SECRET'))
        upload_result = None
        file_to_upload = request.files['file']
        app.logger.info('%s file_to_upload', file_to_upload)
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload)
            app.logger.info(upload_result)
            print (jsonify(upload_result))
            image_url = upload_result["secure_url"]
            new_piece= Piece(image_url = image_url, title=form.title.data, artist=form.artist.data, comments=form.comments.data, user_id=current_user.id)
            # return render_template('gallery.html', piece = new_piece, form=form)
            return redirect(url_for('gallery'))
    else:
        return render_template('add_piece.html', form=form, piece=None)



# image_url = new_piece.image_url

# pieces = Piece.query.all

@app.route('/pieces/<piece_id>/edit', methods=["GET", "POST"])
@login_required
def edit_piece(piece_id):
    piece_to_edit = Piece.query.get_or_404(piece_id)
    form = ImageForm()
    # make sure the post to edit is owned by the current user
    if piece_to_edit.creator != current_user:
        flash("Sorry! You do not have permission to edit this piece. Please sign in or create a separate account", "danger")
        return redirect(url_for('index', piece_id=piece_id))
    if form.validate_on_submit():
        cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
        api_secret=os.getenv('API_SECRET'))
        upload_result = None
        file_to_upload = request.files['file']
        app.logger.info('%s file_to_upload', file_to_upload)
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload)
            app.logger.info(upload_result)
            print (jsonify(upload_result))
            image_url = upload_result["secure_url"]
            title = form.title.data
            artist= form.artist.data
            comments = form.comments.data
            piece_to_edit.update(image_url = image_url, title=title, artist=artist, comments=comments, user_id=current_user.id)
            flash(f"{piece_to_edit.title} has been updated", 'success')
            return redirect(url_for('gallery', piece_id=piece_id))
        else:
            title = form.title.data
            artist= form.artist.data
            comments = form.comments.data
            piece_to_edit.update(title=title, artist=artist, comments=comments, user_id=current_user.id)
            flash(f"{piece_to_edit.title} has been updated", 'success')
        return redirect(url_for('gallery', piece_id=piece_id))
    form.comments.data=piece_to_edit.comments
    return render_template('edit_piece.html', piece=piece_to_edit, form=form)          
        

@app.route('/pieces/<piece_id>/delete')
@login_required
def delete_piece(piece_id):
    piece_to_delete = Piece.query.get_or_404(piece_id)
    if piece_to_delete.creator != current_user:
        flash('You do not have permission to delete this piece', 'danger')
        return redirect(url_for('index'))
    piece_to_delete.delete()
    flash(f"{piece_to_delete.title} has been deleted", 'info')
    return redirect(url_for('portfolio', piece=piece_to_delete))


@app.route('/comments/', methods=['POST','GET'])
def comments():
    comments =Comment.query.order_by(Comment.id.desc()).all()
    return render_template('gallery.html',comments=comments)


@app.route('/comments/<comment_id>/edit-comment', methods=["GET", "POST"])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    form = CommentForm()
    # make sure the post to edit is owned by the current user
    if comment.author != current_user:
        flash("Sorry! You do not have permission to edit this comment", "danger")
        return redirect(url_for('gallery', comment=comment.id))
    if form.validate_on_submit():
        comment.update(text=form.comments.data, user_id=current_user.id)
        flash(f"your comment has been updated", 'success')
        return redirect(url_for('gallery', comment_id=comment_id))
    form.comments.data = comment.text
    return render_template('edit_comment.html', comment=comment, form=form)          
        


@app.route('/comments/<comment_id>/delete')
@login_required
def delete_comment(comment_id):
    comment_to_delete = Comment.query.get_or_404(comment_id)
    if comment_to_delete.author != current_user:
        flash('You do not have permission to delete this comment', 'danger')
        return redirect(url_for('gallery'))
    comment_to_delete.delete()
    flash(f"Your comment has been deleted", 'info')
    return redirect(url_for('gallery', comment=comment_to_delete))

# # oldest comments first
# for comment in Comment.query.order_by(Comment.timestamp.asc()):
#     print('{}: {}'.format(comment.author, comment.text))

# # newest comments first
# for comment in Comment.query.order_by(Comment.timestamp.desc()):
#     print('{}: {}'.format(comment.author, comment.text))


