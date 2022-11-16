from app import db
from app.models.book import Book
from app.models.author import Author
from app.helper_routes import *
from flask import abort, Blueprint, jsonify, make_response, request

authors_bp = Blueprint("authors_bp", __name__,url_prefix="/authors", static_folder='static')

@authors_bp.route("", methods=["POST"])
def create_author():
    request_body = request.get_json()
    new_author = Author.from_dict(request_body)
    
    db.session.add(new_author)
    db.session.commit()
    return jsonify(f"Author {new_author.name} successfully created"), 201


@authors_bp.route("/<author_id>", methods=["GET"])
def read_one_author(author_id):
    author = validate_model(Author, author_id)
    return jsonify(author.to_dict()), 200

@authors_bp.route("", methods=["GET"])
def read_all_authors():

    author_query = request.args.get("author")
    if author_query:
        authors = Author.query.filter_by(name=author_query)
    else:
        authors = Author.query.all()

    authors_response = [author.to_dict() for author in authors]
    return jsonify(authors_response), 200


@authors_bp.route("/<author_id>", methods=["PUT"])
def update_author(author_id):
    author = validate_model(Author, author_id)

    request_body = request.get_json()
    author.name = request_body["name"]
    author.e_mail = request_body["e-mail"]
    author.twitter = request_body["twitter"]

    db.session.commit()
    return jsonify(f"Author #{author.id} successfully updated"), 200


@authors_bp.route("/<author_id>/books", methods=["POST"])
def create_book(author_id):
    author = validate_model(Author, author_id)
    request_body = request.get_json()
    request_body["author_id"] = author.id
    
    new_book = Book.from_dict(request_body)

    db.session.add(new_book)
    db.session.commit()
    return jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201


@authors_bp.route("/<author_id>/books", methods=["GET"])
def read_all_books(author_id):

    author = validate_model(Author, author_id)
    books = Book.query.filter_by(author=author)

    books_response = [book.to_dict() for book in books]
    return jsonify(books_response)