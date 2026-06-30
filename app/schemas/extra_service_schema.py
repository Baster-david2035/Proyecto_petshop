from pydantic import BaseModel

class ServicioSchema(BaseModel):
    id_servicio: int
    nombre: str
    costo: int
    tipo_servicio: str


class ServicioCreateSchema(BaseModel):
    nombre: str
    costo: int
    tipo_servicio: str