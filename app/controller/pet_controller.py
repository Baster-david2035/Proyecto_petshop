from fastapi import APIRouter, HTTPException
from app.service.pet_service import MascotaService
from app.schemas.pet_schema import MascotaSchema, MascotaCreateSchema

router = APIRouter(prefix="/mascotas", tags=["Mascotas"])

service = MascotaService()


@router.post("/", response_model=MascotaSchema)
def crear_mascota(mascota: MascotaCreateSchema):
    """Metodo para agregar una mascota a la tabla de mascotas."""
    try:
        return service.crear(mascota)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[MascotaSchema])
def listar_mascotas():
    return service.obtener_todas()


@router.get("/disponibles", response_model=list[MascotaSchema])
def listar_mascotas_disponibles():
    """Adopcion: solo carga los animalitos disponibles para adoptar."""
    return service.obtener_disponibles()


@router.get("/{id_mascota}", response_model=MascotaSchema)
def obtener_mascota(id_mascota: int):
    mascota = service.obtener_por_id(id_mascota)
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota


@router.patch("/{id_mascota}/estado")
def actualizar_estado(id_mascota: int, estado: str):
    mascota = service.actualizar_estado(id_mascota, estado)
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota


@router.delete("/{id_mascota}")
def eliminar_mascota(id_mascota: int):
    eliminado = service.eliminar(id_mascota)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return {"mensaje": "Mascota eliminada"}
