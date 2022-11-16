from app import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    date = db.Column(db.Date)
    content = db.Column(db.Text)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('reviewer.id'))
    reviewer = db.relationship("Reviewer", back_populates="reviews")
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    book = db.relationship("Book", back_populates="reviews")

    def to_dict(self):
        return {
            "reviewer": self.reviewer.name,
            "book": self.book.title,
            "title": self.title,
            "date": self.date,
            "content": self.content,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            date=data["date"],
            content=data["content"],
            reviewer_id=data["reviewer_id"],
            book_id=data["book_id"],
        )