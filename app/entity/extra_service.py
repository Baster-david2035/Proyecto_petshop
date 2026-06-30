from sqlalchemy import Column, Integer, String, Float
from app.config.database import Base

class ServicioORM(Base):
    __tablename__ = 'servicios_tb'

    id_servicio = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    costo = Column(Float, nullable=False)
    tipo_servicio = Column(String(100), nullable=False)

    def __repr__(self):
        return (
            f"Servicio(id_servicio={self.id_servicio}, "
            f"nombre='{self.nombre}', "
            f"costo={self.precio}, "
            f"tipo='{self.tipo}')"
        )