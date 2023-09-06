"""
The books Blueprint handles the creation, modification, deletion,
and viewing of books for the users of this application.
"""
from flask import Blueprint


books_blueprint = Blueprint('books', __name__, template_folder='templates')

from . import routes
