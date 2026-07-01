from fastapi import APIRouter, HTTPException
from app.service.adoption_service import AdopcionService
from app.schemas.adoption_schema import AdopcionSchema, AdopcionCreateSchema, PagoSchema

router = APIRouter(prefix="/adopciones", tags=["Adopciones"])

service = AdopcionService()


@router.post("/", response_model=AdopcionSchema)
def crear_adopcion(adopcion: AdopcionCreateSchema):
    try:
        return service.create(adopcion)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pagar", response_model=AdopcionSchema)
def pagar_servicios(pago: PagoSchema):
    """
    Servicios: al realizar el pago se guarda la adopcion, se finaliza la
    solicitud y la mascota cambia su estado a 'Adoptada'. Si la solicitud
    ya fue atendida, no se permite volver a pagar.
    """
    try:
        return service.procesar_pago(pago)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[AdopcionSchema])
def listar_adopciones():
    return service.get_all()


@router.get("/{id_adopcion}", response_model=AdopcionSchema)
def obtener_adopcion(id_adopcion: int):
    adopcion = service.get_by_id(id_adopcion)
    if not adopcion:
        raise HTTPException(status_code=404, detail="Adopción no encontrada")
    return adopcion


@router.delete("/{id_adopcion}")
def eliminar_adopcion(id_adopcion: int):
    eliminado = service.delete(id_adopcion)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Adopción no encontrada")
    return {"mensaje": "Adopción eliminada"}


@router.get("/cliente/{id_cliente}")
def adopciones_por_cliente(id_cliente: int):
    return service.get_by_client(id_cliente)


@router.get("/reportes/ganancias")
def ganancias_totales():
    return service.ganancias()
