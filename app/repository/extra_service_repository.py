from app.config.database import SessionLocal
from app.entity.extra_service import ServicioORM

class ServicioExtraRepository:
    def create(self, nombre, costo, tipo):
        with SessionLocal() as db:
            obj = ServicioORM(nombre=nombre, costo=costo, tipo_servicio=tipo)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            db.expunge(obj)
            return obj

    def get(self, id_servicio):
        with SessionLocal() as db:
            return db.query(ServicioORM).filter_by(id_servicio=id_servicio).first()

    def get_all(self):
        with SessionLocal() as db:
            return db.query(ServicioORM).all()

    def delete(self, id_servicio):
        with SessionLocal() as db:
            obj = db.query(ServicioORM).filter_by(id_servicio=id_servicio).first()
            if obj:
                db.delete(obj)
                db.commit()
            return obj
