from pydantic import BaseModel


class SolicitudSchema(BaseModel):
    id_solicitud: int
    id_cliente: int
    id_mascota: int
    motivo: str
    espacio: str
    horas: str
    otra_mascota: str
    estado: str


class SolicitudCreateSchema(BaseModel):
    id_cliente: int
    id_mascota: int
    motivo: str
    espacio: str
    horas: str
    otra_mascota: str
