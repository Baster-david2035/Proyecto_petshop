from datetime import datetime
from app.repository.adoption_repository import AdopcionRepository
from app.repository.solicitud_repository import SolicitudRepository
from app.repository.pet_repository import MascotaRepository
from app.entity.adoption import AdopcionORM

class AdopcionService:
    def __init__(self):
        self.repo = AdopcionRepository()
        self.solicitud_repo = SolicitudRepository()
        self.mascota_repo = MascotaRepository()

    def create(self, adopcion_data):
        adopcion = AdopcionORM(
            id_cliente=adopcion_data.id_cliente,
            id_mascota=adopcion_data.id_mascota,
            fecha_adopcion=str(datetime.now()),
            costo=adopcion_data.costo,
        )
        return self.repo.create(adopcion)

    def procesar_pago(self, pago_data):
        """
        Servicios: apenas se realiza el pago se almacena la adopcion,
        se finaliza la solicitud y se cambia el estado de la mascota a 'Adoptada'.
        Tambien valida que una solicitud ya atendida no se vuelva a pagar.
        """
        solicitud = self.solicitud_repo.get(pago_data.id_solicitud)
        if not solicitud:
            raise ValueError("Solicitud no encontrada")

        if solicitud.estado == "Finalizada":
            raise ValueError("Esta solicitud ya fue atendida y pagada, no puede volver a pagar")

        mascota = self.mascota_repo.get(pago_data.id_mascota)
        if not mascota:
            raise ValueError("Mascota no encontrada")

        adopcion = AdopcionORM(
            id_cliente=pago_data.id_cliente,
            id_mascota=pago_data.id_mascota,
            fecha_adopcion=str(datetime.now()),
            costo=pago_data.costo,
        )
        adopcion = self.repo.create(adopcion)

        self.solicitud_repo.update_estado(pago_data.id_solicitud, "Finalizada")
        self.mascota_repo.update_estado(pago_data.id_mascota, "Adoptada")

        return adopcion

    def get_by_id(self, id_adopcion):
        return self.repo.get_by_id(id_adopcion)

    def get_all(self):
        return self.repo.get_all()

    def get_by_client(self, id_cliente):
        return self.repo.get_by_cliente(id_cliente)

    def delete(self, id_adopcion):
        return self.repo.delete(id_adopcion)

    def ganancias(self):
        return self.repo.total_ganancias()
