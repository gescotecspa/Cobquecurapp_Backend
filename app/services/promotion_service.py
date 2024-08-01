from app import db
from app.models.promotion import Promotion, PromotionImage
from app.models.category import Category

class PromotionService:
    @staticmethod
    def get_promotion_by_id(promotion_id):
        return Promotion.query.get(promotion_id)

    @staticmethod
    def create_promotion(branch_id, title, description, start_date, expiration_date, qr_code, discount_percentage, available_quantity=None, partner_id=None, category_ids=[], image_paths=[]):
        new_promotion = Promotion(
            branch_id=branch_id,
            title=title,
            description=description,
            start_date=start_date,
            expiration_date=expiration_date,
            qr_code=qr_code,
            discount_percentage=discount_percentage,
            available_quantity=available_quantity,
            partner_id=partner_id
        )
        db.session.add(new_promotion)
        for category_id in category_ids:
            category = Category.query.get(category_id)
            if category:
                new_promotion.categories.append(category)
        for path in image_paths:
            new_image = PromotionImage(promotion=new_promotion, image_path=path)
            db.session.add(new_image)
        db.session.commit()
        return new_promotion

    @staticmethod
    def update_promotion(promotion_id, title=None, description=None, start_date=None, expiration_date=None, qr_code=None, discount_percentage=None, available_quantity=None, partner_id=None, branch_id=None, category_ids=None, image_paths=None):
        promotion = PromotionService.get_promotion_by_id(promotion_id)
        if promotion:
            if title:
                promotion.title = title
            if description:
                promotion.description = description
            if start_date:
                promotion.start_date = start_date
            if expiration_date:
                promotion.expiration_date = expiration_date
            if qr_code:
                promotion.qr_code = qr_code
            if discount_percentage is not None:
                promotion.discount_percentage = discount_percentage
            if available_quantity is not None:
                promotion.available_quantity = available_quantity
            if partner_id is not None:
                promotion.partner_id = partner_id
            if branch_id is not None:
                promotion.branch_id = branch_id
            if category_ids is not None:
                promotion.categories.clear()
                for category_id in category_ids:
                    category = Category.query.get(category_id)
                    if category:
                        promotion.categories.append(category)
            if image_paths is not None:
                old_images = PromotionImage.query.filter(PromotionImage.promotion_id == promotion_id).all()
                for old_image in old_images:
                    db.session.delete(old_image)
                for path in image_paths:
                    new_image = PromotionImage(promotion_id=promotion_id, image_path=path)
                    db.session.add(new_image)
            db.session.commit()
        return promotion

    @staticmethod
    def delete_promotion(promotion_id):
        promotion = PromotionService.get_promotion_by_id(promotion_id)
        if promotion:
            db.session.delete(promotion)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_all_promotions():
        return Promotion.query.all()
