from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    website = db.Column(db.String)
    format = db.Column(db.String)
    pages = db.Column(db.Integer)
    publication_date = db.Column(db.Date)
    publisher = db.Column(db.String)
    price = db.Column(db.Float)
    isbn = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), default=None)
    author = db.relationship("Author", back_populates="books")
    reviews = db.relationship("Review", back_populates="book")

    def to_dict(self):
        book_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "website": self.website,
            "format": self.format,
            "pages": self.pages,
            "publication date": self.publication_date,
            "publisher": self.publisher,
            "price": self.price,
            "isbn": self.isbn,
        }

        if self.reviews:
            book_dict["reviews"] = self.get_all_reviews()

        return book_dict

    def get_all_reviews(self):
        return [review.to_dict() for review in self.reviews]

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            description=data["description"],
            website=data["website"],
            format=data["format"],
            pages=data["pages"],
            publication_date = data["publication date"],
            publisher = data["publisher"],
            price = data["price"],
            isbn = data["isbn"],
            author_id = data["author_id"]
        )