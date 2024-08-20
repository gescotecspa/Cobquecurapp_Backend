from app import db
from app.models.status import Status

class StatusLoadService:

    @staticmethod
    def load_statuses():
        if Status.query.count() > 0:
            print("Los estados ya están cargados en la base de datos.")
            return

        # Lista de estados predeterminados
        statuses = ['active', 'inactive', 'suspended', 'deleted']

        for status in statuses:
            new_status = Status(name=status)
            db.session.add(new_status)

        db.session.commit()
        print("Estados cargados exitosamente en la base de datos.")
