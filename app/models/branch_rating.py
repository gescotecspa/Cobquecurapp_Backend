from app import db

class BranchRating(db.Model):
    __tablename__ = 'branch_ratings'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(1000))
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('tourists.user_id'), nullable=False)
    
    branch = db.relationship('Branch', backref='branch_ratings')
    tourist = db.relationship('Tourist', backref='tourist_branch_ratings')

    def serialize(self):
        return {
            'id': self.id,
            'branch_id': self.branch_id,
            'tourist_id': self.tourist_id,
            'rating': self.rating,
            'comment': self.comment
        }
