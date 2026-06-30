from fastapi import APIRouter, HTTPException
from app.service.adoption_service import AdopcionService
from app.schemas.adoption_schema import AdopcionSchema

router = APIRouter(prefix="/adopciones", tags=["Adopciones"])

service = AdopcionService()


@router.post("/", response_model=AdopcionSchema)
def crear_adopcion(adopcion: AdopcionSchema):
    try:
        return service.crear_adopcion(
            adopcion.id_adopcion,
            adopcion.id_cliente,
            adopcion.nombre_cliente,
            adopcion.id_mascota,
            adopcion.nombre_mascota,
            adopcion.fecha_adopcion,
            adopcion.id_servicio,
            adopcion.servicio,
            adopcion.costo
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[AdopcionSchema])
def listar_adopciones():
    return service.listar_adopciones()


@router.get("/{id_adopcion}", response_model=AdopcionSchema)
def obtener_adopcion(id_adopcion: int):
    adopcion = service.buscar_adopcion(id_adopcion)
    if not adopcion:
        raise HTTPException(status_code=404, detail="Adopción no encontrada")
    return adopcion


@router.delete("/{id_adopcion}")
def eliminar_adopcion(id_adopcion: int):
    eliminado = service.eliminar_adopcion(id_adopcion)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Adopción no encontrada")
    return {"mensaje": "Adopción eliminada"}


@router.get("/cliente/{id_cliente}")
def adopciones_por_cliente(id_cliente: int):
    return service.obtener_por_cliente(id_cliente)


@router.get("/reportes/ganancias")
def ganancias_totales():
    return service.obtener_ganancias()