from app import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    e_mail = db.Column(db.String, default=None)
    twitter = db.Column(db.String, default=None)
    books = db.relationship("Book", back_populates="author")

    def to_dict(self):
        author_dict = {
            "id": self.id,
            "author": self.name,
            "e-mail": self.e_mail,
            "twitter": self.twitter,
        }

        if self.books:
            author_dict["books"] = self.get_all_books()

        return author_dict

    def get_all_books(self):
        return [book.to_dict() for book in self.books]


        