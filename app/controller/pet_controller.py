from fastapi import APIRouter, HTTPException
from app.service.pet_service import MascotaService
from app.schemas.pet_schema import MascotaSchema

router = APIRouter(prefix="/mascotas", tags=["Mascotas"])

service = MascotaService()


@router.post("/", response_model=MascotaSchema)
def crear_mascota(mascota: MascotaSchema):
    try:
        return service.crear_mascota(
            mascota.id_mascota,
            mascota.nombre,
            mascota.raza,
            mascota.edad,
            mascota.estado
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[MascotaSchema])
def listar_mascotas():
    return service.listar_mascotas()


@router.get("/{id_mascota}", response_model=MascotaSchema)
def obtener_mascota(id_mascota: int):
    mascota = service.buscar_mascota(id_mascota)
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota


@router.patch("/{id_mascota}/estado")
def actualizar_estado(id_mascota: int, estado: str):
    mascota = service.actualizar_estado(id_mascota, estado)
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota