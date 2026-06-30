from app.config.database import SessionLocal
from app.entity.solicitud import SolicitudORM

class SolicitudRepository:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, solicitud):
        self.db.add(solicitud)
        self.db.commit()
        return solicitud

    def get_all(self):
        return self.db.query(SolicitudORM).all()

    def get(self, id_mascota):
        return self.db.query(SolicitudORM).filter_by(id_mascota=id_mascota).first()

    def update_estado(self, id_mascota, estado):
        solicitud = self.get(id_mascota)
        if solicitud:
            solicitud.estado = estado
            self.db.commit()
        return solicitud