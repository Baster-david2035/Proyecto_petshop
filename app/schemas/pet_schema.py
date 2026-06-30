from pydantic import BaseModel

class MascotaSchema(BaseModel):
    id_mascota: int
    nombre: str
    raza: str
    edad: int
    estado: str


class MascotaCreateSchema(BaseModel):
    nombre: str
    raza: str
    edad: int
    estado: str