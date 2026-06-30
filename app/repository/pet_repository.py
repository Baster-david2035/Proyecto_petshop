from app.config.database import SessionLocal
from app.entity.pet import MascotaORM

class MascotaRepository:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, mascota):
        self.db.add(mascota)
        self.db.commit()
        return mascota

    def get_all(self):
        return self.db.query(MascotaORM).all()

    def get(self, id_mascota):
        return self.db.query(MascotaORM).filter_by(id_mascota=id_mascota).first()

    def update_estado(self, id_mascota, estado):
        mascota = self.get(id_mascota)
        if mascota:
            mascota.estado = estado
            self.db.commit()
        return mascota