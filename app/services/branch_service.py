from app import db
from app.models.branch import Branch
from ..common.image_manager import ImageManager

class BranchService:
    @staticmethod
    def get_branch_by_id(branch_id):
        return Branch.query.get(branch_id)

    @staticmethod
    def create_branch(partner_id, name, description, address, latitude, longitude, status_id, image_data=None):
        # Manejo de la imagen con ImageManager
        image_url = None
        if image_data:
            image_manager = ImageManager()
            filename = f"branches/{name.replace(' ', '_')}_image.png"
            image_url = image_manager.upload_image(image_data, filename)

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
                image_manager = ImageManager()
                filename = f"branches/{branch.name.replace(' ', '_')}_image.png"
                image_url = image_manager.upload_image(image_data, filename)
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
                branch.status_id = status_id  # Asegúrate de que status_id es un entero

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
        return Branch.query.all()

    @staticmethod
    def get_branches_by_partner_id(partner_id):
        return Branch.query.filter_by(partner_id=partner_id).all()
