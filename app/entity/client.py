from sqlalchemy import Column, Integer, String
from app.config.database import Base

class ClienteORM(Base):
    __tablename__ = 'clientes_tb'

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    correo = Column(String(100), nullable=False)

    def __repr__(self):
        return (
            f"Cliente(id_cliente={self.id_cliente}, "
            f"nombre='{self.nombre}', "
            f"telefono='{self.telefono}', "
            f"correo='{self.correo}')"
        )