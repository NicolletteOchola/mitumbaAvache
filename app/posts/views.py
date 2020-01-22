import os
from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint, current_app)
from flask_login import current_user, login_required, logout_user
from app import db, bcrypt
import secrets
from PIL import Image
from app.request import get_quote
from app.models import Post, User, Comment
from app.posts.forms import PostForm, CommentForm
from app.request import get_quote
from flask_simplemde import SimpleMDE
from ..main import views


posts = Blueprint('posts', __name__)
quotes = get_quote()


def save_picture(form_image):
    randome_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_image.filename)
    picture_name = randome_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/featured_images', picture_name)
    
    output_size = (1000, 400)
    final_image = Image.open(form_image)
    final_image.thumbnail(output_size)
    
    final_image.save(picture_path)
    
    return picture_name

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    
    if form.validate_on_submit():
        pic =None
        if form.image.data:
            picture_file = save_picture(form.image.data)
            final_pic = picture_file
            pic= final_pic
        post = Post(title=form.title.data, content=form.content.data, author=current_user, category=form.category.data, image=pic)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been published!', 'success')
        return redirect(url_for('main.home'))
    
    myposts = Post.query.order_by(Post.posted_date.desc())
    return render_template('new-post.html', title='New Post', form=form, legend='New Post', myposts=myposts, quotes=quotes)


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id = post_id).all()
    myposts = Post.query.order_by(Post.posted_date.desc())
    return render_template('post.html', title=post.title, post=post, comments = comments, myposts=myposts, quotes=quotes)
