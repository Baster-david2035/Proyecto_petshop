from sqlalchemy import Column, Integer, String
from app.config.database import Base

class MascotaORM(Base):
    __tablename__ = 'mascotas_tb'

    id_mascota = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(20), nullable=False)
    raza = Column(String(20), nullable=False)
    edad = Column(Integer, nullable=False)
    estado = Column(String(30),nullable=False)  # Disponible / Adoptada

    def __repr__(self):
        return (
            f"Mascota(id_mascota={self.id_mascota}, "
            f"nombre='{self.nombre}', "
            f"raza='{self.raza}', "
            f"edad={self.edad}, "
            f"estado='{self.estado}')"
        )