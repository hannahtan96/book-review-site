from app import db

class Reviewer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    reviews = db.relationship("Review", back_populates="reviewer")

    def to_dict(self):
        reviewer_dict = {
            "id": self.id,
            "name": self.name
        }

        if self.reviews:
            reviewer_dict["reviews"] = self.get_all_reviews()

        return reviewer_dict

    def get_all_reviews(self):
        return [review.to_dict() for review in self.reviews]