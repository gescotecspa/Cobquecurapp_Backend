from app import db

class TouristRating(db.Model):
    __tablename__ = 'tourist_ratings'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1000))
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'), nullable=False)
    tourist_id = db.Column(db.Integer, db.ForeignKey('tourists.user_id'), nullable=False)

    branch = db.relationship('Branch', backref='tourist_branch_ratings')
    tourist = db.relationship('Tourist', backref='tourist_ratings')

    # __table_args__ = (
    #     db.UniqueConstraint('branch_id', 'tourist_id', name='_branch_tourist_uc'),
    # )

    def serialize(self):
        return {
            'id': self.id,
            'branch_id': self.branch_id,
            'tourist_id': self.tourist_id,
            'rating': self.rating,
            'comment': self.comment
        }
