from app import db

# Definición de la tabla de asociación para SQLAlchemy
tourist_categories = db.Table('tourist_categories',
    db.Column('user_id', db.Integer, db.ForeignKey('tourists.user_id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)
)

class Tourist(db.Model):
    __tablename__ = 'tourists'

    user_id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(255))
    birthday = db.Column(db.Date)
    gender = db.Column(db.String(50))
    # Establecemos la relación sólo de Tourist hacia Category, sin backref.
    categories = db.relationship('Category', secondary=tourist_categories, lazy='dynamic')

    def serialize(self):
        return {
            "user_id": self.user_id,
            "origin": self.origin,
            "birthday": self.birthday.isoformat() if self.birthday else None,
            "gender": self.gender,
            #"categories": [category.category_id for category in self.categories]
            "categories": [{"id": category.category_id, "name": category.name} for category in self.categories]

        }

    def __repr__(self):
        return f"<Tourist {self.user_id}: {self.origin}, Birthday: {self.birthday}, Gender: {self.gender}>"