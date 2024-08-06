from app import db
from app.models import BranchRating

class BranchRatingService:
    @staticmethod
    def get_rating_by_branch_and_tourist(branch_id, user_id):
        # Devuelve la valoración de la sucursal hecha por un turista específico
        return BranchRating.query.filter_by(branch_id=branch_id, user_id=user_id).first()

    @staticmethod
    def create_rating(branch_id, user_id, rating, comment=None):
        # Crea una nueva valoración para una sucursal por un turista
        existing_rating = BranchRatingService.get_rating_by_branch_and_tourist(branch_id, user_id)
        if existing_rating:
            return None  # Ya existe una valoración para esta combinación

        new_rating = BranchRating(branch_id=branch_id, user_id=user_id, rating=rating, comment=comment)
        db.session.add(new_rating)
        db.session.commit()
        return new_rating

    @staticmethod
    def update_rating(rating_id, rating, comment):
        try:
            # Busca la calificación por su ID
            rating_record = BranchRating.query.get(rating_id)
            if rating_record:
                rating_record.rating = rating
                rating_record.comment = comment
                db.session.commit()
                return rating_record
            return None
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_rating(rating_id):
        try:
            # Busca y elimina la calificación por su ID
            rating_record = BranchRating.query.get(rating_id)
            if rating_record:
                db.session.delete(rating_record)
                db.session.commit()
                return rating_record
            return None
        except Exception as e:
            db.session.rollback()
            raise e
    @staticmethod
    def get_all_ratings_for_branch(branch_id):
        return BranchRating.query.filter_by(branch_id=branch_id).all()
    
    @staticmethod
    def get_average_rating_for_branch(branch_id):
        ratings = BranchRating.query.filter_by(branch_id=branch_id).all()
        if not ratings:
            return 0
        total_rating = sum(rating.rating for rating in ratings)
        return total_rating / len(ratings)
