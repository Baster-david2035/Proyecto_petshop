from fastapi import APIRouter, HTTPException
from app.service.extra_service_service import ServicioExtraService
from app.schemas.extra_service_schema import ServicioSchema

router = APIRouter(prefix="/servicios", tags=["Servicios"])

service = ServicioExtraService()


@router.post("/", response_model=ServicioSchema)
def crear_servicio(servicio: ServicioSchema):
    try:
        return service.crear_servicio(
            servicio.id_servicio,
            servicio.nombre,
            servicio.costo,
            servicio.tipo_servicio
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ServicioSchema])
def listar_servicios():
    return service.listar_servicios()


@router.get("/{id_servicio}", response_model=ServicioSchema)
def obtener_servicio(id_servicio: int):
    servicio = service.buscar_servicio(id_servicio)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio