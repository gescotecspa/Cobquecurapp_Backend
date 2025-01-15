from app.models import db, Favorite

class FavoriteService:
    @staticmethod
    def add_favorite(user_id, promotion_id):
        # Verificar si el usuario existe
        tourist = Tourist.query.get(user_id)
        if not tourist:
            raise ValueError("User not found.")

        # Verificar si la promoción existe
        promotion = Promotion.query.get(promotion_id)
        if not promotion:
            raise ValueError("Promotion not found.")

        # Verificar si el favorito ya existe
        favorite = Favorite.query.filter_by(user_id=user_id, promotion_id=promotion_id).first()
        if favorite:
            return None  # Retornar None si ya existe

        # Crear nuevo favorito
        new_favorite = Favorite(user_id=user_id, promotion_id=promotion_id)
        db.session.add(new_favorite)
        db.session.commit()
        return new_favorite


    @staticmethod
    def remove_favorite(user_id, promotion_id):
        favorite = Favorite.query.filter_by(user_id=user_id, promotion_id=promotion_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_favorites_by_tourist(user_id):
        return Favorite.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_favorites_by_promotion(promotion_id):
        return Favorite.query.filter_by(promotion_id=promotion_id).all()