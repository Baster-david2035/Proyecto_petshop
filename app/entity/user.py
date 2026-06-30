from sqlalchemy import Column, String
from app.config.database import Base

class UsuarioORM(Base):
    __tablename__ = 'usuarios_tb'

    nombre_usuario = Column(String(50), primary_key=True)
    contrasena = Column(String(100), nullable=False)

    def __repr__(self):
        return f"Usuario(nombre_usuario='{self.nombre_usuario}')"