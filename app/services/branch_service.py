from app import db
from app.models.branch import Branch

class BranchService:
    @staticmethod
    def get_branch_by_id(branch_id):
        return Branch.query.get(branch_id)

    @staticmethod
    def create_branch(partner_id, name, description, address, latitude, longitude, status, image_url=None):
        new_branch = Branch(
            partner_id=partner_id,
            name=name,
            description=description,
            address=address,
            latitude=latitude,
            longitude=longitude,
            status=status,
            image_url=image_url
        )
        db.session.add(new_branch)
        db.session.commit()
        return new_branch

    @staticmethod
    def update_branch(branch_id, partner_id=None, name=None, description=None, address=None, latitude=None, longitude=None, status=None, image_url=None):
        branch = BranchService.get_branch_by_id(branch_id)
        if branch:
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
            if status:
                branch.status = status
            if image_url:
                branch.image_url = image_url 
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
