from app import db

class Branch(db.Model):
    __tablename__ = 'branches'

    branch_id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner_details.user_id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False)  
    image_url = db.Column(db.String(255)) 
    partner = db.relationship('Partner', back_populates='branches')
    promotions = db.relationship('Promotion', backref='branch', lazy=True, cascade='all, delete-orphan')
    status = db.relationship('Status') 

    def serialize(self):
        return {
            "branch_id": self.branch_id,
            "partner_id": self.partner_id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "status": self.status.serialize() if self.status else None,
            "image_url": self.image_url,
        }

    def __repr__(self):
        return f'<Branch {self.name}>'