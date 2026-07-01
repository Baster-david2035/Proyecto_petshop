from sqlalchemy import Column, Integer, String, ForeignKey
from app.config.database import Base

class SolicitudORM(Base):
    __tablename__ = 'solicitudes_tb'

    id_solicitud = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, nullable=False)
    id_mascota = Column(Integer, nullable=False)
    motivo = Column(String(50), nullable=False)
    espacio = Column(String(20), nullable=False)
    horas = Column(String(20), nullable=False)
    otra_mascota = Column(String(30), nullable=False)
    estado = Column(String(30),nullable=False)  # En revision / Aprobada / Rechazada / Finalizada

    def __repr__(self):
        return (
            f"Solicitud NO: {self.id_solicitud}"
            f"Cliente(id_cliente={self.id_cliente}, "
            f"Mascota(id_mascota={self.id_mascota}, "
            f"Motivo: '{self.motivo}', "
            f"Espacio disponible:'{self.espacio}', "
            f"horas: {self.horas}, "
            f"otra_mascota:'{self.otra_mascota}'),"
            f"estado: {self.estado}"
        )