from flask import (abort, current_app, flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required
from pydantic import BaseModel, ValidationError, validator

from project import db
from project.models import Book

from . import books_blueprint


# --------------
# Helper Classes
# --------------

class BookModel(BaseModel):
    """Class for parsing new book data from a form."""
    title: str
    author: str
    rating: int

    @validator('rating')
    def book_rating_check(cls, value):
        if value not in range(1, 6):
            raise ValueError('Book rating must be a whole number between 1 and 5')
        return value


# ------
# Routes
# ------

@books_blueprint.route('/')
def index():
    # If the user is already logged in, redirect to the list of books
    if current_user.is_authenticated:
        return redirect(url_for('books.list_books'))

    return render_template('books/index.html')


@books_blueprint.get('/books/')
@login_required
def list_books():
    query = db.select(Book).where(Book.user_id == current_user.id).order_by(Book.id)
    books = db.session.execute(query).scalars().all()
    return render_template('books/books.html', books=books)


@books_blueprint.route('/books/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        try:
            book_data = BookModel(
                title=request.form['book_title'],
                author=request.form['book_author'],
                rating=request.form['book_rating']
            )
            print(book_data)

            # Save the form data to the database
            new_book = Book(book_data.title, book_data.author, book_data.rating, current_user.id)
            db.session.add(new_book)
            db.session.commit()

            flash(f"Added new book ({new_book.title})!")
            current_app.logger.info(f'Book ({new_book.title}) was added for user: {current_user.id}!')
            return redirect(url_for('books.list_books'))
        except ValidationError as e:
            flash("Error with book data submitted!")
            print(e)

    return render_template('books/add_book.html')


@books_blueprint.route('/books/<id>/delete')
@login_required
def delete_book(id):
    query = db.select(Book).where(Book.id == id)
    book = db.session.execute(query).scalar_one_or_none()

    if book is None:
        abort(404)

    if book.user_id != current_user.id:
        abort(403)

    db.session.delete(book)
    db.session.commit()
    flash(f'Book ({book.title}) was deleted!')
    current_app.logger.info(f'Book ({book.title}) was deleted for user: {current_user.id}!')
    return redirect(url_for('books.list_books'))


@books_blueprint.route('/books/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    query = db.select(Book).where(Book.id == id)
    book = db.session.execute(query).scalar_one_or_none()

    if book is None:
        abort(404)

    if book.user_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        # Edit the book data in the database
        book.update(request.form['book_title'],
                    request.form['book_author'],
                    request.form['book_rating'])
        db.session.add(book)
        db.session.commit()

        flash(f'Book ({ book.title }) was updated!')
        current_app.logger.info(f'Book ({ book.title }) was updated by user: { current_user.id}')
        return redirect(url_for('books.list_books'))

    return render_template('books/edit_book.html', book=book)
