from app.config.database import SessionLocal
from app.entity.pet import MascotaORM

class MascotaRepository:
    def create(self, mascota: MascotaORM):
        with SessionLocal() as db:
            db.add(mascota)
            db.commit()
            db.refresh(mascota)
            db.expunge(mascota)
            return mascota

    def get_all(self):
        with SessionLocal() as db:
            return db.query(MascotaORM).all()

    def get_disponibles(self):
        with SessionLocal() as db:
            return db.query(MascotaORM).filter_by(estado="Disponible").all()

    def get(self, id_mascota):
        with SessionLocal() as db:
            return db.query(MascotaORM).filter_by(id_mascota=id_mascota).first()

    def update_estado(self, id_mascota, estado):
        with SessionLocal() as db:
            mascota = db.query(MascotaORM).filter_by(id_mascota=id_mascota).first()
            if mascota:
                mascota.estado = estado
                db.commit()
                db.refresh(mascota)
                db.expunge(mascota)
            return mascota

    def delete(self, id_mascota):
        with SessionLocal() as db:
            obj = db.query(MascotaORM).filter_by(id_mascota=id_mascota).first()
            if obj:
                db.delete(obj)
                db.commit()
            return obj
