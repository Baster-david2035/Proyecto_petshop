from app.config.database import SessionLocal
from app.entity.client import ClienteORM

class ClienteRepository:
    def create(self, cliente: ClienteORM):
        with SessionLocal() as db:
            db.add(cliente)
            db.commit()
            db.refresh(cliente)
            db.expunge(cliente)
            return cliente

    def exist(self, id_cliente):
        with SessionLocal() as db:
            return db.query(ClienteORM).filter_by(id_cliente=id_cliente).first() is not None

    def get_by_correo(self, correo):
        with SessionLocal() as db:
            return db.query(ClienteORM).filter_by(correo=correo).first()

    def get_all(self):
        with SessionLocal() as db:
            return db.query(ClienteORM).all()

    def get(self, id_cliente):
        with SessionLocal() as db:
            return db.query(ClienteORM).filter_by(id_cliente=id_cliente).first()

    def delete(self, id_cliente):
        with SessionLocal() as db:
            obj = db.query(ClienteORM).filter_by(id_cliente=id_cliente).first()
            if obj:
                db.delete(obj)
                db.commit()
            return obj
