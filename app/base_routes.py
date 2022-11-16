from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, render_template

base_bp = Blueprint("base_bp", __name__, url_prefix="/", static_folder='static')

@base_bp.route("", methods=["GET"])
def read_home_page():
    books = Book.query.all()
    return render_template('base.html', books=books)

@base_bp.route("contact", methods=["GET"])
def read_contact_page():
    return render_template('contact.html')