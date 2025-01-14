from app import db
from app.models.app_version import AppVersion
from sqlalchemy.exc import SQLAlchemyError

class AppVersionService:

    @staticmethod
    def get_version_by_id(version_id):
        try:
            version = AppVersion.query.get(version_id)
            return version
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error al obtener la versión: {e}")
            return None

    @staticmethod
    def update_version(version_id, version_number, platform, release_date, download_url, notes, is_active, is_required):
        try:
            version = AppVersion.query.get(version_id)
            if not version:
                return None

            version.version_number = version_number
            version.platform = platform
            version.release_date = release_date
            version.download_url = download_url
            version.notes = notes
            version.is_active = is_active
            version.is_required = is_required

            db.session.commit()
            return version
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error al actualizar la versión: {e}")
            return None

    @staticmethod
    def delete_version(version_id):
        try:
            version = AppVersion.query.get(version_id)
            if version:
                db.session.delete(version)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error al eliminar la versión: {e}")
            return False

    @staticmethod
    def get_all_versions():
        try:
            versions = AppVersion.query.all()
            return versions
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error al obtener todas las versiones: {e}")
            return []

    @staticmethod
    def create_version(version_number, platform, release_date, download_url, notes, is_active, is_required):
        try:
            version = AppVersion(
                version_number=version_number,
                platform=platform,
                release_date=release_date,
                download_url=download_url,
                notes=notes,
                is_active=is_active,
                is_required=is_required
            )
            db.session.add(version)
            db.session.commit()
            return version
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error al crear la versión: {e}")
            return None

    @staticmethod
    def get_active_version(platform):
        try:
            # Traemos la versión activa y obligatoria más reciente según la fecha de creación del registro
            version = AppVersion.query.filter_by(platform=platform, is_active=True, is_required=True) \
                .order_by(AppVersion.created_at.desc()).first()
            return version
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error al obtener la versión activa para {platform}: {e}")
            return None

