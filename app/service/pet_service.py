from app.repository.pet_repository import MascotaRepository
from app.entity.pet import MascotaORM

class MascotaService:
    def __init__(self):
        self.repo = MascotaRepository()

    def crear(self, mascota_data):
        mascota = MascotaORM(
            nombre=mascota_data.nombre,
            raza=mascota_data.raza,
            edad=mascota_data.edad,
            estado=mascota_data.estado or "Disponible",
        )
        return self.repo.create(mascota)

    def obtener_todas(self):
        return self.repo.get_all()

    def obtener_disponibles(self):
        """Adopcion: solo carga los animalitos disponibles para adoptar."""
        return self.repo.get_disponibles()

    def obtener_por_id(self, id_mascota):
        return self.repo.get(id_mascota)

    def actualizar_estado(self, id_mascota, estado):
        mascota = self.repo.get(id_mascota)
        if not mascota:
            return None
        return self.repo.update_estado(id_mascota, estado)

    def eliminar(self, id_mascota):
        return self.repo.delete(id_mascota)
