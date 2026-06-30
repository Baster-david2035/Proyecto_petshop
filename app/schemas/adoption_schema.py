from pydantic import BaseModel

class AdopcionSchema(BaseModel):
    id_adopcion: int
    id_cliente: int
    id_mascota: int
    fecha_adopcion: str
    costo: int


class AdopcionCreateSchema(BaseModel):
    id_cliente: int
    id_mascota: int
    fecha_adopcion: str
    costo: int