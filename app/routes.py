from app import app, db
from flask import render_template, redirect, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from urllib.parse import urlsplit
import sqlalchemy as sa
from app.models import User, Author, Book
from app.forms import LoginForm, RegistrationForm, AuthorForm, NewBookForm

"""Login and Registration"""
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
        user = User(username=form.username.data, password=passwordHash, role=form.role.data)
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

"""Authors"""
@app.route("/authors") 
@login_required
def authors():
    authors = db.session.scalars(sa.select(Author)).all()
    return render_template("Authors/Authors.html", title='Authors', authors=authors)

@app.route("/add_author", methods=['GET','POST'])
@login_required
def add_author():
    form = AuthorForm()
    if form.validate_on_submit():
        author = Author(name=form.name.data, age=form.age.data)
        db.session.add(author)
        db.session.commit()
        flash('Author added to the database.')
        return redirect(url_for('authors'))
    return render_template("Authors/Add.html", title='Add Author', form=form)

@app.route("/view_author/<id>")
@login_required
def view_author(id):
    author = db.first_or_404(sa.select(Author).where(Author.author_id == id))
    books = db.session.scalars(author.authored_books()).all()
    return render_template("Authors/View.html", title="Author Details", author=author, books=books)

@app.route("/edit_author/<id>", methods=['GET','POST'])
@login_required
def edit_author(id):
    form = AuthorForm()
    if form.validate_on_submit():
        cmd = sa.update(Author).where(Author.author_id == id).values(name=form.name.data, age=form.age.data)
        db.session.execute(cmd)
        db.session.commit()
        flash('Author added to the database.')
        return redirect(url_for('authors'))
    elif request.method == 'GET':
        author = db.first_or_404(sa.select(Author).where(Author.author_id == id))
        form.name.data = author.name
        form.age.data = author.age
    return render_template("Authors/Edit.html", title='Edit Author', form=form, id=id)

@app.route("/delete_author/<id>")
@login_required
def delete_author(id):
    cmd = sa.delete(Author).where(Author.author_id == id)
    db.session.execute(cmd)
    db.session.commit()
    return redirect(url_for('authors'))

"""Books"""
@app.route("/books") 
@login_required
def books():
    books = db.session.scalars(sa.select(Book)).all()
    return render_template("Books/Books.html", books=books)   

@app.route("/add_book")
@login_required
def add_book():
    return "Hello, World"

@app.route("/edit_book")
@login_required
def edit_book():
    return "Hello, World"

@app.route("/delete_book")
@login_required
def delete_book():
    return "Hello, World"                                     