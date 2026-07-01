from pydantic import BaseModel
from typing import Optional


class UsuarioSchema(BaseModel):
    nombre_usuario: str
    id_cliente: Optional[int] = None


class RegistroSchema(BaseModel):
    """Registro: guarda cliente y usuario al mismo tiempo."""
    nombre: str
    telefono: str
    correo: str
    contrasena: str


class LoginSchema(BaseModel):
    correo: str
    contrasena: str


class LoginResponseSchema(BaseModel):
    mensaje: str
    es_admin: bool
    id_cliente: Optional[int] = None
    nombre: Optional[str] = None
    correo: Optional[str] = None


class RecuperarSchema(BaseModel):
    correo: str
    nueva_contrasena: str
