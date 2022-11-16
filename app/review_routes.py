from app import db
from app.models.book import Book
from app.models.review import Review
from app.models.reviewer import Reviewer
from app.helper_routes import *
from flask import abort, Blueprint, jsonify, make_response, request

reviews_bp = Blueprint("reviews_bp", __name__,url_prefix="/reviews", static_folder='static')


@reviews_bp.route("", methods=["POST"])
def create_review():
    request_body = request.get_json()
    if request_body.get("reviewer"):
        reviewer = return_reviewer_from_name(request_body["reviewer"])
        request_body["reviewer_id"] = reviewer.id
    if request_body.get("book"):
        book = return_book_from_name(request_body["book"])
        request_body["book_id"] = book.id

    new_review = Review.from_dict(request_body)
    db.session.add(new_review)
    db.session.commit()

    return jsonify(f"Review for {new_review.book.title} written by {new_review.reviewer.name} successfully created"), 201


@reviews_bp.route("", methods=["GET"])
def read_all_reviews():
    reviews = Review.query.all()

    reviews_response = [review.to_dict() for review in reviews]
    return jsonify(reviews_response), 200


@reviews_bp.route("/<review_id>", methods=["GET"])
def read_one_review(review_id):
    review = validate_model(Review, review_id)
    return jsonify(review.to_dict()), 200



@reviews_bp.route("/<review_id>", methods=["PATCH"])
def update_review(review_id):
    request_body = request.get_json()
    review_to_update = validate_model(Review, review_id)
    if request_body.get("reviewer"):
        reviewer = return_reviewer_from_name(request_body["reviewer"])
        request_body["reviewer_id"] = reviewer.id
    if request_body.get("book"):
        book = return_book_from_name(request_body["book"])
        request_body["book_id"] = book.id

    for elem in request_body:
        if elem == 'reviewer_id':
            review_to_update.reviewer_id = request_body["reviewer_id"]
        elif elem == 'book':
            review_to_update.book_id = request_body["book_id"]
        elif elem == 'title':
            review_to_update.title = request_body['title']
        elif elem == 'date':
            review_to_update.date = request_body['date']
        elif elem == 'content':
            review_to_update.content = request_body['content']

    db.session.commit()
    return jsonify({"msg": f"Review #{review_to_update.id} successfully updated"}), 200
