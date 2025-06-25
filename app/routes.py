from app import app, db
from flask import render_template, redirect, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from urllib.parse import urlsplit
import sqlalchemy as sa
from app.models import User
from app.forms import LoginForm, RegistrationForm

"""User Management"""

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template("Login.html", title='Log In', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        passwordHash = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=passwordHash, role='User')
        db.session.add(user)
        db.session.commit()
        flash('User registered successfully, please log in.')
        return redirect(url_for('login'))
    return render_template("Register.html", title='Register', form=form)

"""Home"""
@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template("Home.html", title='Home')                                                 