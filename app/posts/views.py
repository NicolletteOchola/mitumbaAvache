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