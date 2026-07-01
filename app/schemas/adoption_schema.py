from pydantic import BaseModel


class AdopcionSchema(BaseModel):
    id_adopcion: int
    id_cliente: int
    id_mascota: int
    fecha_adopcion: str
    costo: float


class AdopcionCreateSchema(BaseModel):
    id_cliente: int
    id_mascota: int
    costo: float


class PagoSchema(BaseModel):
    """Se usa cuando el cliente paga los servicios y se confirma la adopcion."""
    id_cliente: int
    id_mascota: int
    id_solicitud: int
    costo: float
