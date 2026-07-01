from fastapi import APIRouter, HTTPException
from app.service.solicitud_service import SolicitudService
from app.schemas.solicitud_schema import SolicitudSchema, SolicitudCreateSchema

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])

service = SolicitudService()

@router.post("/", response_model=SolicitudSchema)
def crear_solicitud(solicitud: SolicitudCreateSchema):
    """Adopcion: el boton de solicitud envia los valores del formulario."""
    try:
        return service.crear(solicitud)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[SolicitudSchema])
def listar_solicitudes():
    return service.obtener_todos()

@router.get("/cliente/{id_cliente}", response_model=list[SolicitudSchema])
def solicitudes_por_cliente(id_cliente: int):
    """Home: el cliente ve en tiempo real el estado de sus solicitudes."""
    return service.obtener_por_cliente(id_cliente)

@router.get("/{id_solicitud}", response_model=SolicitudSchema)
def obtener_solicitud(id_solicitud: int):
    solicitud = service.obtener_por_id(id_solicitud)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return solicitud

@router.patch("/{id_solicitud}/estado")
def actualizar_estado(id_solicitud: int, estado: str):
    solicitud = service.actualizar_estado(id_solicitud, estado)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return solicitud
