from app.models.user import User
from app import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def create_user(password, first_name, last_name, country, email, status, city=None, birth_date=None, phone_number=None, gender=None, subscribed_to_newsletter=None, image_url=None):
        existing_user = UserService.get_user_by_email(email)
        if existing_user:
            raise ValueError("A user with that email already exists.")

        hashed_password = generate_password_hash(password)
        new_user = User(password=hashed_password, first_name=first_name, last_name=last_name, country=country, email=email, status=status, city=city, birth_date=birth_date, phone_number=phone_number, gender=gender, subscribed_to_newsletter=subscribed_to_newsletter, image_url=image_url)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("A database error occurred, possibly duplicated data.")
        return new_user

    @staticmethod
    def update_user(user_id, **kwargs):
        user = UserService.get_user_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        return None

    @staticmethod
    def delete_user(user_id):
        user = UserService.get_user_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False