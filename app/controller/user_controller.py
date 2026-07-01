from fastapi import APIRouter, HTTPException
from app.service.user_service import UsuarioService
from app.schemas.user_schema import (
    UsuarioSchema,
    RegistroSchema,
    LoginSchema,
    LoginResponseSchema,
    RecuperarSchema,
)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

service = UsuarioService()


@router.post("/registro")
def registro(data: RegistroSchema):
    """Registro: guarda el cliente y el usuario al mismo tiempo, con sus validaciones."""
    try:
        return service.registrar(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=LoginResponseSchema)
def login(usuario: LoginSchema):
    """Login: valida que el usuario exista y pueda ingresar. Incluye validacion de admin."""
    resultado = service.login(usuario.correo, usuario.contrasena)
    if not resultado:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return resultado


@router.patch("/recuperar")
def recuperar(data: RecuperarSchema):
    """Recuperar: restaura la contrasena segun el correo electronico."""
    try:
        return service.recuperar_contrasena(data.correo, data.nueva_contrasena)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=list[UsuarioSchema])
def get_usuarios():
    return service.get_all()
