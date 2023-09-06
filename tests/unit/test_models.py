"""
This file (test_models.py) contains the unit tests for the models.py file.
"""
from project.models import Book, User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password_hashed, authenticated, and active fields are defined correctly
    """
    user = User('patkennedy79@gmail.com', 'FlaskIsAwesome')
    assert user.email == 'patkennedy79@gmail.com'
    assert user.password_hashed != 'FlaskIsAwesome'
    assert user.__repr__() == '<User: patkennedy79@gmail.com>'
    assert user.is_authenticated
    assert user.is_active
    assert not user.is_anonymous


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password_hashed fields are defined correctly
    """
    assert new_user.email == 'patkennedy79@gmail.com'
    assert new_user.password_hashed != 'FlaskIsAwesome'


def test_setting_password(new_user):
    """
    GIVEN an existing User
    WHEN the password for the user is set
    THEN check the password is stored correctly and not as plaintext
    """
    new_user.set_password('MyNewPassword')
    assert new_user.password_hashed != 'MyNewPassword'
    assert new_user.is_password_correct('MyNewPassword')
    assert not new_user.is_password_correct('MyNewPassword2')
    assert not new_user.is_password_correct('FlaskIsAwesome')


def test_user_id(new_user):
    """
    GIVEN an existing User
    WHEN the ID of the user is defined to a value
    THEN check the user ID returns a string (and not an integer) as needed by Flask-WTF
    """
    new_user.id = 17
    assert isinstance(new_user.get_id(), str)
    assert not isinstance(new_user.get_id(), int)
    assert new_user.get_id() == '17'


def test_new_book():
    """
    GIVEN a Book model
    WHEN a new Book is created
    THEN check the title, author, and rating fields are defined correctly
    """
    book = Book('Malibu Rising', 'Taylor Jenkins Reid', '5', 1)
    assert book.title == 'Malibu Rising'
    assert book.author == 'Taylor Jenkins Reid'
    assert book.rating == 5
    assert book.__repr__() == '<Book: Malibu Rising>'


def test_update_book():
    """
    GIVEN a Book model
    WHEN a new Book is updated
    THEN check the title, author, and rating fields are updated correctly
    """
    book = Book('Malibu Rising', 'Taylor Jenkins Reid', '5', 1)

    book.update(new_title='Carrie Soto is Back')
    assert book.title == 'Carrie Soto is Back'
    assert book.author == 'Taylor Jenkins Reid'
    assert book.rating == 5

    book.update(new_rating='4')
    assert book.title == 'Carrie Soto is Back'
    assert book.author == 'Taylor Jenkins Reid'
    assert book.rating == 4

    book.update(new_author='Taylor J. Reid')
    assert book.title == 'Carrie Soto is Back'
    assert book.author == 'Taylor J. Reid'
    assert book.rating == 4

    book.update(new_title='Book Lovers', new_author='Emily Henry', new_rating='5')
    assert book.title == 'Book Lovers'
    assert book.author == 'Emily Henry'
    assert book.rating == 5
