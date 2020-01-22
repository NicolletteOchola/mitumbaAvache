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
