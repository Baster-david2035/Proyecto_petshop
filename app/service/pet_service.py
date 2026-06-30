from app.repository.pet_repository import MascotaRepository

class MascotaService:
    def __init__(self):
        self.repo = MascotaRepository()

    def create(self, mascota):
        return self.repo.agregar(mascota)

    def get_all(self):
        return self.repo.obtener_todos()

    def update_status(self, id_mascota, estado):
        mascota = self.repo.buscar_por_id(id_mascota)
        if not mascota:
            return None
        mascota.estado = estado
        return self.repo.guardar()