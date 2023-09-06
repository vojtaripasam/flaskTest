from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from project import db


class User(UserMixin, db.Model):
    """
    Class that represents a user of the application

    The following attributes of a user are stored in this table:
        * email - email address of the user
        * hashed password - hashed password (using werkzeug.security)
        * registered_on - date & time that the user registered

    REMEMBER: Never store the plaintext password in a database!
    """

    __tablename__ = 'users'

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    email = mapped_column(String(), unique=True, nullable=False)
    password_hashed = mapped_column(String(128), nullable=False)
    registered_on = mapped_column(DateTime(), nullable=False)

    # Define the relationship to the `Book` class
    books_relationship = relationship('Book', back_populates='user_relationship')

    def __init__(self, email: str, password_plaintext: str):
        """Create a new User object using the email address and hashing the
        plaintext password using Werkzeug.Security.
        """
        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext)
        self.registered_on = datetime.now()

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    def set_password(self, password_plaintext: str):
        self.password_hashed = self._generate_password_hash(password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f'<User: {self.email}>'


class Book(db.Model):
    """
    Class that represents a book that has been read.

    The following attributes of a book are stored in this table:
        * title - title of the book
        * author - author of the book
        * rating - rating (1 (bad) to 5 (amazing)) of the book
    """

    __tablename__ = 'books'

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    title = mapped_column(String())
    author = mapped_column(String())
    rating = mapped_column(Integer())
    user_id = mapped_column(ForeignKey('users.id'))

    # Define the relationship to the `User` class
    user_relationship = relationship('User', back_populates='books_relationship')

    def __init__(self, book_title: str, book_author: str, book_rating: str, book_user_id: int):
        """Create a new Book object using the title, author, and rating of the book."""
        self.title = book_title
        self.author = book_author
        self.rating = int(book_rating)
        self.user_id = book_user_id

    def update(self, new_title: str = '', new_author: str = '', new_rating: str = ''):
        """Update the fields of the Book object."""
        if new_title:
            self.title = new_title
        if new_author:
            self.author = new_author
        if new_rating:
            self.rating = int(new_rating)

    def __repr__(self):
        return f'<Book: {self.title}>'
