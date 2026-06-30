from app.config.database import SessionLocal
from app.entity.user import UsuarioORM

class UsuarioRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_by_username(self, username):
        return self.db.query(UsuarioORM).filter_by(nombre_usuario=username).first()

    def create(self, username, password):
        user = UsuarioORM(nombre_usuario=username, contrasena=password)
        self.db.add(user)
        self.db.commit()
        return user

    def get_all(self):
        return self.db.query(UsuarioORM).all()