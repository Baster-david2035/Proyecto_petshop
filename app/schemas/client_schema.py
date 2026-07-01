from pydantic import BaseModel


class ClienteSchema(BaseModel):
    id_cliente: int
    nombre: str
    telefono: str
    correo: str
    estado: str


class ClienteCreateSchema(BaseModel):
    nombre: str
    telefono: str
    correo: str
