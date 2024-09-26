from app import db
from app.models.terms_and_conditions import TermsAndConditions
from datetime import datetime
from app.models.user import User

class TermsAndConditionsService:

    @staticmethod
    def get_latest_version():
        return TermsAndConditions.query.order_by(TermsAndConditions.created_at.desc()).first()

    @staticmethod
    def get_all_terms():
        return TermsAndConditions.query.all()

    @staticmethod
    def get_terms_by_id(terms_id):
        return TermsAndConditions.query.get(terms_id)

    @staticmethod
    def create_terms(content, version):
        new_terms = TermsAndConditions(content=content, version=version)
        db.session.add(new_terms)
        db.session.commit()
        return new_terms

    @staticmethod
    def update_terms(terms_id, content, version):
        terms = TermsAndConditions.query.get(terms_id)
        if terms:
            terms.content = content
            terms.version = version
            db.session.commit()
            return terms
        return None

    @staticmethod
    def delete_terms(terms_id):
        terms = TermsAndConditions.query.get(terms_id)
        if terms:
            db.session.delete(terms)
            db.session.commit()
            return True
        return False

    @staticmethod
    def accept_terms(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found.")
        
        latest_terms = TermsAndConditionsService.get_latest_version()
        if not latest_terms:
            raise ValueError("No terms available.")
        
        user.terms_id = latest_terms.id
        user.terms_accepted_at = datetime.utcnow()
        
        db.session.commit()
        return user