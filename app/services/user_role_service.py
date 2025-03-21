from app import db
from app.models import UserRole, User, Role
from app.models.tourist import Tourist
from app.services.tourist_service import TouristService

class UserRoleService:
    @staticmethod
    def add_role_to_user(user_id, role_id):
        # Obtener el usuario y el rol
        user = User.query.get(user_id)
        role = Role.query.get(role_id)

        # Verificar si el usuario y el rol existen
        if user and role:
            # Si se asigna el rol de "turista", verificar si el usuario ya tiene un registro en la tabla tourist
            if role.role_name == "tourist":
                tourist = Tourist.query.filter_by(user_id=user_id).first()

                # Si no tiene un registro en la tabla tourist, se crea uno utilizando el servicio de creación de turistas
                if not tourist:
                    # Puedes añadir parámetros adicionales si es necesario (por ejemplo, 'origin', 'birthday', etc.)
                    tourist = TouristService.create_tourist(
                        user_id=user_id,
                        origin=user.country,
                        birthday=user.birth_date,
                        gender=user.gender,
                        category_ids=[]
                    )

            # Asignar el rol al usuario sin eliminar el rol anterior ni modificar la tabla 'partner'
            user_role = UserRole(user_id=user_id, role_id=role_id)
            db.session.add(user_role)
            db.session.commit()
            return user_role

        return None

    @staticmethod
    def remove_role_from_user(user_id, role_id):
        user_role = UserRole.query.filter_by(user_id=user_id, role_id=role_id).first()
        if user_role:
            db.session.delete(user_role)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_roles_for_user(user_id):
        return UserRole.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_users_for_role(role_id):
        return UserRole.query.filter_by(role_id=role_id).all()
    
    @staticmethod
    def clear_roles_for_user(user_id):
        db.session.query(UserRole).filter_by(user_id=user_id).delete()
        db.session.commit()