# models.py

from app import db

class Metric(db.Model):
    __tablename__ = 'metrics'

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Date, nullable=False)
    total_users = db.Column(db.Integer, nullable=False, default=0)
    growth_percentage = db.Column(db.Float, nullable=False, default=0.0)
    viewed_offers = db.Column(db.Integer, nullable=False, default=0)
    redeemed_offers = db.Column(db.Integer, nullable=False, default=0)
    conversion_rate = db.Column(db.Float, nullable=False, default=0.0)
    category = db.Column(db.String(255), nullable=False, default='Desconocido')
    published_offers_avg = db.Column(db.Float, nullable=False, default=0.0)
    available_coupons = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, 
                 month, 
                 total_users=0, 
                 growth_percentage=0.0, 
                 viewed_offers=0, 
                 redeemed_offers=0, 
                 conversion_rate=0.0, 
                 category='Desconocido', 
                 published_offers_avg=0.0, 
                 available_coupons=0):
        self.month = month
        self.total_users = total_users
        self.growth_percentage = growth_percentage
        self.viewed_offers = viewed_offers
        self.redeemed_offers = redeemed_offers
        self.conversion_rate = conversion_rate
        self.category = category
        self.published_offers_avg = published_offers_avg
        self.available_coupons = available_coupons

    def __repr__(self):
        return f"<Metric id={self.id} month={self.month} total_users={self.total_users}>"
