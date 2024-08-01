from app import db

# Definición de la tabla de asociación
partner_categories = db.Table('partner_categories',
    db.Column('partner_user_id', db.Integer, db.ForeignKey('partner_details.user_id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)
)

class Partner(db.Model):
    __tablename__ = 'partner_details'

    user_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.Text, nullable=False)
    contact_info = db.Column(db.String(255), nullable=False)
    business_type = db.Column(db.String(255))
    categories = db.relationship('Category', secondary=partner_categories, lazy='dynamic')
    branches = db.relationship('Branch', back_populates='partner', cascade='all, delete-orphan')  # Añadir esta línea

    def serialize(self):
        return {
            "user_id": self.user_id,
            "address": self.address,
            "contact_info": self.contact_info,
            "business_type": self.business_type,
            "categories": [{"category_id": category.category_id, "name": category.name} for category in self.categories]
        }

    def __repr__(self):
        return f"<Partner {self.user_id}: {self.address}, Contact: {self.contact_info}, Business Type: {self.business_type}>"
