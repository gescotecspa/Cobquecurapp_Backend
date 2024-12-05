from app import db
from app.models.branch import Branch
from app.models.status import Status
from ..common.image_manager import ImageManager
from datetime import datetime
from app.services.promotion_service import PromotionService

class BranchService:
    @staticmethod
    def get_branch_by_id(branch_id):
        return Branch.query.get(branch_id)

    @staticmethod
    def create_branch(partner_id, name, description, address, latitude, longitude, status_id, image_data=None):
        # Manejo de la imagen con ImageManager
        image_url = None
        if image_data:
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            image_manager = ImageManager()
            filename = f"branches/{partner_id}/{name.replace(' ', '_')}_image_{timestamp}.png"  # Cambiar aquí
            category = 'branches'
            image_url = image_manager.upload_image(image_data, filename, category)

        new_branch = Branch(
            partner_id=partner_id,
            name=name,
            description=description,
            address=address,
            latitude=latitude,
            longitude=longitude,
            status_id=status_id,
            image_url=image_url
        )
        db.session.add(new_branch)
        db.session.commit()
        return new_branch

    @staticmethod
    def update_branch(branch_id, partner_id=None, name=None, description=None, address=None, latitude=None, longitude=None, status_id=None, image_data=None):
        branch = BranchService.get_branch_by_id(branch_id)
        if branch:
            # Manejo de la imagen con ImageManager en la actualización
            if image_data:
                timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
                image_manager = ImageManager()
                filename = f"branches/{partner_id}/{name.replace(' ', '_')}_image_{timestamp}.png"
                category = 'branches'
                image_url = image_manager.upload_image(image_data, filename, category)
                branch.image_url = image_url

            if partner_id is not None:
                branch.partner_id = partner_id
            if name:
                branch.name = name
            if description:
                branch.description = description
            if address:
                branch.address = address
            if latitude is not None:
                branch.latitude = latitude
            if longitude is not None:
                branch.longitude = longitude
            if status_id is not None:
                # Verificar si el estado cambió
                if branch.status_id != status_id:
                    # Buscar los estados 'inactive' y 'active'
                    inactive_status = Status.query.filter_by(name='inactive').first()
                    active_status = Status.query.filter_by(name='active').first()
                    
                    if not inactive_status or not active_status:
                        raise ValueError("Inactive or Active status not found in the database.")

                    # Actualizar el estado de las promociones asociadas
                    if status_id == inactive_status.id:
                        # Cambiar promociones a 'inactive'
                        promotion_ids = [promo.promotion_id for promo in branch.promotions]
                        # print("ids de las promociones a inactivar",promotion_ids)
                        PromotionService.bulk_update_promotions_status(promotion_ids, inactive_status.id)
                    elif status_id == active_status.id:
                        # Cambiar promociones a 'active'
                        promotion_ids = [promo.promotion_id for promo in branch.promotions]
                        # print("ids de las promociones a activar",promotion_ids)
                        PromotionService.bulk_update_promotions_status(promotion_ids, active_status.id)

                    # Actualizar el estado de la sucursal
                    branch.status_id = status_id

            db.session.commit()
        return branch

    @staticmethod
    def delete_branch(branch_id):
        branch = BranchService.get_branch_by_id(branch_id)
        if branch:
            db.session.delete(branch)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_all_branches():
        return (
            Branch.query.join(Status)
            .filter(Status.name != 'deleted')
            .all()
        )

    @staticmethod
    def get_branches_by_partner_id(partner_id):
        return Branch.query.filter_by(partner_id=partner_id).all()
