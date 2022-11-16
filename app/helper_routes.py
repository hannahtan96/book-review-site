from app import db
from app.models.book import Book
from app.models.author import Author
from app.models.reviewer import Reviewer
from flask import abort, Blueprint, jsonify, make_response, request

books_bp = Blueprint("books_bp", __name__,url_prefix="/books")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} \'{model_id}\' is invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    return model


# handle error message if book does not currently exist
def return_book_from_name(book):
    chosen_book = Book.query.filter(Book.title==book).first()
    if chosen_book is None:
        abort(make_response({"message": f"Book {book} not found"}, 404))
    else:
        return chosen_book

# handle creation of new author instance if author does not currently exist
def return_author_from_name(author):
    chosen_author = Author.query.filter(Author.name==author).first()
    if chosen_author is None:
        new_author = Author(name=author)
        
        db.session.add(new_author)
        db.session.commit()
        return new_author
    else:
        return chosen_author


# handle creation of new reviewer instance if reviewer does not currently exist
def return_reviewer_from_name(reviewer):
    chosen_reviewer = Reviewer.query.filter(Reviewer.name==reviewer).first()
    if chosen_reviewer is None:
        new_reviewer = reviewer.from_dict({"name":reviewer})
        
        db.session.add(new_reviewer)
        db.session.commit()
        return new_reviewer
    else:
        return chosen_reviewer