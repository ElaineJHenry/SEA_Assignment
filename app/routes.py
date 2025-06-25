from app import app, db
from flask import render_template, redirect, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
import sqlalchemy as sa
from app.models import User
from app.forms import LoginForm

"""User Management"""

@app.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    return render_template("Login.html", title='Log In', form=form)

@app.route("/login", methods=['POST'])
def submit_login():
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

@app.route("/register")
def register():
    return render_template("Register.html", title='Register')

@app.route("/register", methods=['POST'])
def submit_registration():
    #code
    return redirect(url_for('login'))

"""Home"""
@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template("Home.html", title='Home')                                                 