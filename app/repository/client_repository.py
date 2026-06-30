from app.config.database import SessionLocal
from app.entity.client import ClienteORM

class ClienteRepository:
    def __init__(self):
        self.db = SessionLocal()

    def create(self, cliente):
        self.db.add(cliente)
        self.db.commit()
        return cliente
    
    def exist(self, id_cliente):
        cliente = self.db.query(ClienteORM).filter_by(id_cliente=id_cliente).first()
        if cliente:
            return True
        return False

    def get_all(self):
        return self.db.query(ClienteORM).all()

    def get(self, id_cliente):
        return self.db.query(ClienteORM).filter_by(id_cliente=id_cliente).first()

    def delete(self, id_cliente):
        obj = self.get(id_cliente)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj