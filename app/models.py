from datetime import date
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True)
    password: so.Mapped[str] = so.mapped_column(sa.String(256))
    role: so.Mapped[str] = so.mapped_column(sa.String(64))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Author(db.Model):
    author_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    age: so.Mapped[int] = so.mapped_column()

    books: so.WriteOnlyMapped['Book'] = so.relationship(back_populates='author')

    def __repr__(self):
        return '<Author {}>'.format(self.name)
    
    def authored_books(self):
        return (sa.select(Book)
                .join(Book.author)
                .where(Book.author_id == self.author_id))


class Book(db.Model):
    book_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    author_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Author.author_id))
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    release_date: so.Mapped[date] = so.mapped_column()
    genre: so.Mapped[str] = so.mapped_column(sa.String(64))
    pages: so.Mapped[int] = so.mapped_column()

    author: so.Mapped[Author] = so.relationship(back_populates='books')

    def __repr__(self):
        return '<Book {}>'.format(self.name)
