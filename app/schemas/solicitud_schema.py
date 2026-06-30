from pydantic import BaseModel

class SolicitudSchema(BaseModel):
    id_mascota: int
    motivo: str 
    espacio: str
    horas: str
    otra_mascota: str
    estado: str


class SolicitudCreateSchema(BaseModel):
    id_mascota: int
    motivo: str 
    espacio: str
    horas: str
    otra_mascota: str
    estado: str
