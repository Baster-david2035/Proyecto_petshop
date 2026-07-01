from app.config.database import SessionLocal
from app.entity.adoption import AdopcionORM
from sqlalchemy import func

class AdopcionRepository:
    def create(self, adopcion: AdopcionORM):
        with SessionLocal() as db:
            db.add(adopcion)
            db.commit()
            db.refresh(adopcion)
            db.expunge(adopcion)
            return adopcion

    def get_all(self):
        with SessionLocal() as db:
            return db.query(AdopcionORM).all()

    def get_by_id(self, id_adopcion):
        with SessionLocal() as db:
            return db.query(AdopcionORM).filter_by(id_adopcion=id_adopcion).first()

    def delete(self, id_adopcion):
        with SessionLocal() as db:
            adopcion = db.query(AdopcionORM).filter_by(id_adopcion=id_adopcion).first()
            if not adopcion:
                return False
            db.delete(adopcion)
            db.commit()
            return True

    def get_by_cliente(self, id_cliente):
        with SessionLocal() as db:
            return db.query(AdopcionORM).filter_by(id_cliente=id_cliente).all()

    def total_ganancias(self):
        with SessionLocal() as db:
            return db.query(func.sum(AdopcionORM.costo)).scalar()
