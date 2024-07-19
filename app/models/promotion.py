from app import db


promotion_categories = db.Table('promotion_categories',
    db.Column('promotion_id', db.Integer, db.ForeignKey('promotions.promotion_id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)
)
class Promotion(db.Model):
    __tablename__ = 'promotions'

    promotion_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    qr_code = db.Column(db.Text, nullable=False)
    partner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    images = db.relationship('PromotionImage', backref='promotion', lazy=True)
    categories = db.relationship('Category', secondary='promotion_categories', backref=db.backref('promotions', lazy=True))

    def serialize(self):
        return {
            "promotion_id": self.promotion_id,
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "expiration_date": self.expiration_date.isoformat() if self.expiration_date else None,
            "qr_code": self.qr_code,
            "partner_id": self.partner_id,
            "images": [image.serialize() for image in self.images],
            "categories": [{"category_id": category.category_id, "name": category.name} for category in self.categories]
        }
    
class PromotionImage(db.Model):
    __tablename__ = 'promotion_images'

    image_id = db.Column(db.Integer, primary_key=True)
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotions.promotion_id'))
    image_path = db.Column(db.Text, nullable=False)

    def serialize(self):
        return {
            "image_id": self.image_id,
            "promotion_id": self.promotion_id,
            "image_path": self.image_path
        }