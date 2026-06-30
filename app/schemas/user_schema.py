from pydantic import BaseModel

class UsuarioSchema(BaseModel):
    nombre_usuario: str
    contrasena: str