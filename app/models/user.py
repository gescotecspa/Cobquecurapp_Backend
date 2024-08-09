from app import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120))
    birth_date = db.Column(db.String(10))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    status = db.Column(db.String(20), nullable=False)
    subscribed_to_newsletter = db.Column(db.Boolean)
    image_url = db.Column(db.String(250))
    reset_code = db.Column(db.String(8), nullable=True)
    reset_code_expiration = db.Column(db.DateTime, nullable=True)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'country': self.country,
            'city': self.city,
            'birth_date': self.birth_date,
            'email': self.email,
            'phone_number': self.phone_number,
            'gender': self.gender,
            'status': self.status,
          'subscribed_to_newsletter': self.subscribed_to_newsletter,
            'image_url': self.image_url
        }