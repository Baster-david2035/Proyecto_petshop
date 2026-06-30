from fastapi import APIRouter, HTTPException
from app.service.user_service import UsuarioService
from app.schemas.user_schema import UsuarioSchema

router = APIRouter(prefix="/auth", tags=["Autenticación"])

service = UsuarioService()


@router.post("/login")
def login(usuario: UsuarioSchema):
    if service.login(usuario.nombre_usuario, usuario.contrasena):
        return {"mensaje": "Login exitoso"}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")