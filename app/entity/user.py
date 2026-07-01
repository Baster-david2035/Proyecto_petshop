from sqlalchemy import Column, String, Integer
from app.config.database import Base

class UsuarioORM(Base):
    __tablename__ = 'usuarios_tb'

    nombre_usuario = Column(String(50), primary_key=True)  # Es el mismo correo del cliente
    contrasena = Column(String(100), nullable=False)
    id_cliente = Column(Integer, nullable=True)  # Relacion con clientes_tb (None para admin)

    def __repr__(self):
        return f"Usuario(nombre_usuario='{self.nombre_usuario}')"