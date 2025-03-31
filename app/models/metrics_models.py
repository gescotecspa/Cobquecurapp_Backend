from app import db

class MetricsUser(db.Model):
    __tablename__ = 'metrics_users'

    month = db.Column(db.Date, primary_key=True)
    total_users = db.Column(db.Integer, nullable=False, default=0)
    growth_percentage = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return f"<MetricsUser month={self.month} total_users={self.total_users}>"


class MetricsPromotion(db.Model):
    __tablename__ = 'metrics_promotions'

    category = db.Column(db.String(255), primary_key=True)
    promotion_count = db.Column(db.Integer, nullable=False, default=0)
    published_percentage = db.Column(db.Float, nullable=False, default=0.0)
    consumed_count = db.Column(db.Integer, nullable=False, default=0)
    consumed_percentage = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return f"<MetricsPromotion category={self.category} promotion_count={self.promotion_count}>"


class MetricsActivity(db.Model):
    __tablename__ = 'metrics_activity'

    category = db.Column(db.String(255), primary_key=True)
    promotion_count = db.Column(db.Integer, nullable=False, default=0)
    active_partners = db.Column(db.Integer, nullable=False, default=0)
    avg_promotions_per_active_partner = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return f"<MetricsActivity category={self.category} active_partners={self.active_partners}>"
