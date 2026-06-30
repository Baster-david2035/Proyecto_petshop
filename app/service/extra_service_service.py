from app.repository.extra_service_repository import ServicioExtraRepository

class ServicioExtraService:
    def __init__(self):
        self.repo = ServicioExtraRepository()

    def create(self, nombre, costo, tipo):
        return self.repo.create(nombre, costo, tipo)

    def get_all(self):
        return self.repo.get_all()

    def get(self, id_servicio):
        return self.repo.get(id_servicio)

    def delete(self, id_servicio):
        return self.repo.delete(id_servicio)