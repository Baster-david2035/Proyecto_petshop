from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.config.database import Base

class AdopcionORM(Base):
    __tablename__ = 'adopciones_tb'

    id_adopcion = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, nullable=False)
    id_mascota = Column(Integer, nullable=False)
    fecha_adopcion = Column(String(50), nullable=False)
    costo = Column(Float, nullable=False)

    def __repr__(self):
        return (
            f"Adopcion(id_adopcion={self.id_adopcion}, "
            f"cliente='{self.nombre_cliente}', "
            f"mascota='{self.nombre_mascota}', "
            f"servicio='{self.servicio}', "
            f"fecha='{self.fecha_adopcion}', "
            f"costo={self.costo})"
        )