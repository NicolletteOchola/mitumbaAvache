import os
from .. import mail
from flask import render_template, url_for, flash, redirect, request, Blueprint, url_for, current_app
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Post, Comment
from app.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm)
import secrets
from PIL import Image
from flask_mail import Message
from ..email import mail_message
from app.request import get_quote

# from app import mail

users = Blueprint('users', __name__)
quotes = get_quote()


@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data, password=form.password.data)
        user.save_user()
        try:
            msg = Message('Hello! Welcome to PITCH. We are glad you joined us.', sender=(
                'nicoleochola@gmail.com'))
            msg.add_recipient(user.email)
            mail.send(msg)
        except Exception as e:
            print('failed')
        return redirect(url_for('users.login'))
        flash('Your account has been created! You are now able to log in', 'success')
        title = "New Account"
    return render_template('register.html', title='Register', form=form, quotes=quotes)