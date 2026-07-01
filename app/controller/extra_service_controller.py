from fastapi import APIRouter, HTTPException
from app.service.extra_service_service import ServicioExtraService
from app.schemas.extra_service_schema import ServicioSchema, ServicioCreateSchema

router = APIRouter(prefix="/servicios", tags=["Servicios"])

service = ServicioExtraService()


@router.post("/", response_model=ServicioSchema)
def crear_servicio(servicio: ServicioCreateSchema):
    """Metodo para agregar un servicio a la tabla de servicios."""
    try:
        return service.create(
            servicio.nombre,
            servicio.costo,
            servicio.tipo_servicio
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ServicioSchema])
def listar_servicios():
    """Servicios: muestra la tabla de servicios actuales."""
    return service.get_all()


@router.get("/{id_servicio}", response_model=ServicioSchema)
def obtener_servicio(id_servicio: int):
    servicio = service.get(id_servicio)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio


@router.delete("/{id_servicio}")
def eliminar_servicio(id_servicio: int):
    eliminado = service.delete(id_servicio)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return {"mensaje": "Servicio eliminado"}
