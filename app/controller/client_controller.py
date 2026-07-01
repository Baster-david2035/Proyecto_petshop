from fastapi import APIRouter, HTTPException
from app.service.client_service import ClienteService
from app.schemas.client_schema import ClienteSchema, ClienteCreateSchema

router = APIRouter(prefix="/clientes", tags=["Clientes"])

service = ClienteService()


@router.post("/", response_model=ClienteSchema)
def crear_cliente(cliente: ClienteCreateSchema):
    """Metodo para agregar un cliente a la tabla de clientes (estado siempre Activo)."""
    try:
        return service.create(cliente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ClienteSchema])
def listar_clientes():
    return service.get_all()


@router.get("/{id_cliente}", response_model=ClienteSchema)
def obtener_cliente(id_cliente: int):
    cliente = service.get(id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.delete("/{id_cliente}")
def eliminar_cliente(id_cliente: int):
    eliminado = service.delete(id_cliente)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"mensaje": "Cliente eliminado"}
