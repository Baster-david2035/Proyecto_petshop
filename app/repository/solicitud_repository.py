from app.config.database import SessionLocal
from app.entity.solicitud import SolicitudORM

class SolicitudRepository:
    def create(self, solicitud: SolicitudORM):
        with SessionLocal() as db:
            db.add(solicitud)
            db.commit()
            db.refresh(solicitud)
            db.expunge(solicitud)
            return solicitud

    def get_all(self):
        with SessionLocal() as db:
            return db.query(SolicitudORM).all()

    def get(self, id_solicitud):
        with SessionLocal() as db:
            return db.query(SolicitudORM).filter_by(id_solicitud=id_solicitud).first()

    def get_by_cliente(self, id_cliente):
        with SessionLocal() as db:
            return db.query(SolicitudORM).filter_by(id_cliente=id_cliente).all()

    def update_estado(self, id_solicitud, estado):
        with SessionLocal() as db:
            solicitud = db.query(SolicitudORM).filter_by(id_solicitud=id_solicitud).first()
            if solicitud:
                solicitud.estado = estado
                db.commit()
                db.refresh(solicitud)
                db.expunge(solicitud)
            return solicitud
