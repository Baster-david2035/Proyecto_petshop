from app.repository.solicitud_repository import SolicitudRepository

class SolicitudService:
    def __init__(self):
        self.repo = SolicitudRepository()

    def crear(self, solicitud):
        return self.repo.create(solicitud)

    def obtener_todos(self):
        return self.repo.get_all()
    
    def obtener_por_id(self, id_mascota):
        return self.repo.get(id_mascota)

    def actualizar_estado(self, id_mascota, estado):
        solicitud = self.repo.get(id_mascota)
        if not solicitud:
            return None
        return self.repo.update_estado(id_mascota, estado)