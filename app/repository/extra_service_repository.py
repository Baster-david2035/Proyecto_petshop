from app.config.database import SessionLocal
from app.entity.extra_service import ServicioORM

class ServicioExtraRepository:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, nombre, costo, tipo):
        obj = ServicioORM(nombre=nombre, costo=costo, tipo_servicio=tipo)
        self.db.add(obj)
        self.db.commit()
        return obj

    def get(self, id_servicio):
        return self.db.query(ServicioORM).filter_by(id_servicio=id_servicio).first()

    def get_all(self):
        return self.db.query(ServicioORM).all()

    def delete(self, id_servicio):
        obj = self.get(id_servicio)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj