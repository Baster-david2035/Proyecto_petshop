from app.repository.solicitud_repository import SolicitudRepository
from app.entity.solicitud import SolicitudORM

class SolicitudService:
    def __init__(self):
        self.repo = SolicitudRepository()

    def crear(self, solicitud_data):
        """Adopcion: los valores del formulario se guardan ligados al cliente y la mascota."""
        solicitud = SolicitudORM(
            id_cliente=solicitud_data.id_cliente,
            id_mascota=solicitud_data.id_mascota,
            motivo=solicitud_data.motivo,
            espacio=solicitud_data.espacio,
            horas=solicitud_data.horas,
            otra_mascota=solicitud_data.otra_mascota,
            estado="En revision",
        )
        return self.repo.create(solicitud)

    def obtener_todos(self):
        return self.repo.get_all()

    def obtener_por_id(self, id_solicitud):
        return self.repo.get(id_solicitud)

    def obtener_por_cliente(self, id_cliente):
        """Home: para que el cliente vea en tiempo real el estado de sus solicitudes."""
        return self.repo.get_by_cliente(id_cliente)

    def actualizar_estado(self, id_solicitud, estado):
        solicitud = self.repo.get(id_solicitud)
        if not solicitud:
            return None
        return self.repo.update_estado(id_solicitud, estado)
