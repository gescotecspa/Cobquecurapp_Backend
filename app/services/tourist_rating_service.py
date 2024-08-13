from app import db
from app.models import TouristRating

class TouristRatingService:
    @staticmethod
    def get_rating_by_tourist_and_branch(tourist_id, branch_id):
        return TouristRating.query.filter_by(tourist_id=tourist_id, branch_id=branch_id).first()

    @staticmethod
    def create_rating(tourist_id, branch_id, rating, comment=None):
        existing_rating = TouristRatingService.get_rating_by_tourist_and_branch(tourist_id, branch_id)
        if existing_rating:
            # Devolver None o lanzar una excepción si ya existe la valoración
            return None, 'Rating already exists for this branch and tourist'

        new_rating = TouristRating(tourist_id=tourist_id, branch_id=branch_id, rating=rating, comment=comment)
        db.session.add(new_rating)
        db.session.commit()
        return new_rating, None
    
    @staticmethod
    def update_rating(rating_id, rating, comment=None):
        existing_rating = TouristRating.query.get(rating_id)
        if existing_rating:
            existing_rating.rating = rating
            existing_rating.comment = comment
            db.session.commit()
            return existing_rating
        return None

    @staticmethod
    def delete_rating(rating_id):
        existing_rating = TouristRating.query.get(rating_id)
        if existing_rating:
            db.session.delete(existing_rating)
            db.session.commit()
            return existing_rating
        return None

    @staticmethod
    def get_all_ratings_for_tourist(tourist_id):
        return TouristRating.query.filter_by(tourist_id=tourist_id).all()

    @staticmethod
    def get_average_rating_for_tourist(tourist_id):
        ratings = TouristRating.query.filter_by(tourist_id=tourist_id).all()
        if ratings:
            return sum(r.rating for r in ratings) / len(ratings)
        return 0
