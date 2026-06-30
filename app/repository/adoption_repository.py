from app.config.database import SessionLocal
from app.entity.adoption import AdopcionORM
from sqlalchemy import func

class AdopcionRepository:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, adopcion):
        self.db.add(adopcion)
        self.db.commit()
        return adopcion

    def get_all(self):
        return self.db.query(AdopcionORM).all()
    
    def get_by_id(self, id_adopcion):
        adopcion = self.db.query(AdopcionORM).filter_by(id_adopcion=id_adopcion).first()
        if not adopcion:
            return None
        return adopcion
    
    def delete(self, id_adopcion):
        adopcion = self.db.query(AdopcionORM).filter_by(id_adopcion=id_adopcion).first()
        if not adopcion:
            return False
        self.db.delete(adopcion)
        self.db.commit()
        return True 

    def get_by_cliente(self, id_cliente):
        return self.db.query(AdopcionORM).filter_by(id_cliente=id_cliente).all()

    def total_ganancias(self):
        return self.db.query(func.sum(AdopcionORM.costo)).scalar()