from app.config.database import SessionLocal
from app.entity.user import UsuarioORM

class UsuarioRepository:
    def get_by_username(self, username):
        with SessionLocal() as db:
            return db.query(UsuarioORM).filter_by(nombre_usuario=username).first()

    def create(self, username, password, id_cliente=None):
        with SessionLocal() as db:
            user = UsuarioORM(nombre_usuario=username, contrasena=password, id_cliente=id_cliente)
            db.add(user)
            db.commit()
            db.refresh(user)
            db.expunge(user)
            return user

    def get_all(self):
        with SessionLocal() as db:
            return db.query(UsuarioORM).all()

    def update_password(self, username, nueva_contrasena):
        with SessionLocal() as db:
            user = db.query(UsuarioORM).filter_by(nombre_usuario=username).first()
            if not user:
                return None
            user.contrasena = nueva_contrasena
            db.commit()
            db.refresh(user)
            db.expunge(user)
            return user
