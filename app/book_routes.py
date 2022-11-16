from app import db
from app.models.book import Book
from app.models.author import Author
from app.helper_routes import *
from flask import abort, Blueprint, jsonify, make_response, render_template, request

books_bp = Blueprint("books_bp", __name__,url_prefix="/books", static_folder='static')


@books_bp.route("", methods=["POST"])
def create_book():
    # use request object info on the http request
    # request.get_json() will "pythonify" the JSON HTTP request body by converting it into a Python dictionary
    request_body = request.get_json()
    if request_body.get("author"):
        author = return_author_from_name(request_body["author"])
        request_body["author_id"] = author.id
    
    new_book = Book.from_dict(request_body)
    db.session.add(new_book)
    db.session.commit()

    return jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201


@books_bp.route("", methods=["GET"])
def read_all_books():
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

    books_response = [book.to_dict() for book in books]
    return jsonify(books_response), 200


@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_model(Book, book_id)

    reviews = [review.to_dict() for review in book.reviews]
    book_response_without_reviews = book.to_dict()
    del book_response_without_reviews["reviews"]
    del book_response_without_reviews["id"]

    # return jsonify(book.to_dict()), 200
    return render_template('eloquent-ruby.html', book=book, description=book_response_without_reviews, reviews=reviews)


@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()
    if request_body.get("author"):
        author = return_author_from_name(request_body.get("author")).id
    elif request_body.get("author_id"):
        author = validate_model(Author, request_body.get("author_id"))
    else:
        author = None

    try:
        book.title = request_body["title"],
        book.description = request_body["description"],
        book.website = request_body["website"],
        book.format=request_body["format"],
        book.pages=request_body["pages"],
        book.publication_date = request_body["publication date"],
        book.publisher = request_body["publisher"],
        book.price = request_body["price"],
        book.isbn = request_body["isbn"]
        book.author = author
    except ValueError:
        return jsonify({"msg": f"missing data"}), 400

    db.session.commit()
    return jsonify({"msg": f"Book #{book.title} successfully updated"}), 200


@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_model(Book, book_id)

    db.session.delete(book)
    db.session.commit()

    return jsonify(f"Book #{book.id} successfully deleted"), 202




