from app import db
from app.models.book import Book
from app.models.review import Review
from app.models.reviewer import Reviewer
from app.helper_routes import *
from flask import abort, Blueprint, jsonify, make_response, request

reviewers_bp = Blueprint("reviewers_bp", __name__,url_prefix="/reviewers", static_folder='static')

@reviewers_bp.route("", methods=["POST"])
def create_reviewer():
    request_body = request.get_json()
    new_reviewer = Reviewer(name=request_body["name"])
    
    db.session.add(new_reviewer)
    db.session.commit()
    return jsonify(f"Reviewer {new_reviewer.name} successfully created"), 201


@reviewers_bp.route("/<reviewer_id>", methods=["GET"])
def read_one_reviewer(reviewer_id):
    reviewer = validate_model(Reviewer, reviewer_id)
    return jsonify(reviewer.to_dict()), 200

@reviewers_bp.route("", methods=["GET"])
def read_all_reviewers():
    name_query = request.args.get("name")
    if name_query:
        reviewers = Reviewer.query.filter_by(name=name_query)
    else:
        reviewers = Reviewer.query.all()

    reviewers_response = [reviewer.to_dict() for reviewer in reviewers]
    return jsonify(reviewers_response), 200


@reviewers_bp.route("/<reviewer_id>", methods=["PUT"])
def update_review(reviewer_id):
    reviewer = validate_model(Reviewer, reviewer_id)

    request_body = request.get_json()
    reviewer.name = request_body["name"]

    db.session.commit()
    return jsonify(f"Reviewer #{reviewer.id} successfully updated"), 204


@reviewers_bp.route("/<reviewer_id>/reviews", methods=["POST"])
def create_review(reviewer_id):
    reviewer = validate_model(Reviewer, reviewer_id)
    request_body = request.get_json()
    request_body["reviewer_id"] = reviewer.id
    request_body["book_id"] = return_book_from_name(request_body["book"]).id
    
    new_review = Review.from_dict(request_body)

    db.session.add(new_review)
    db.session.commit()
    return jsonify(f"Review for {new_review.book.title} written by {new_review.reviewer.name} successfully created"), 201


@reviewers_bp.route("/<reviewer_id>/reviews", methods=["GET"])
def read_all_reviews(reviewer_id):
    reviewer = validate_model(Reviewer, reviewer_id)
    return jsonify(reviewer.to_dict()), 200