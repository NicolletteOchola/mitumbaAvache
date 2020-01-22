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


@users.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    # import pdb; pdb.set_trace()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        # import pdb; pdb.set_trace()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=login_form, quotes=quotes)