from app.repository.pet_repository import MascotaRepository

class MascotaService:
    def __init__(self):
        self.repo = MascotaRepository()

    def crear(self, mascota):
        return self.repo.create(mascota)

    def obtener_todas(self):
        return self.repo.get_all()
    
    def obtener_por_id(self, id_mascota):
        return self.repo.get(id_mascota)

    def actualizar_estado(self, id_mascota, estado):
        mascota = self.repo.get(id_mascota)
        if not mascota:
            return None
        return self.repo.update_estado(id_mascota, estado)