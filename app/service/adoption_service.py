from datetime import datetime
from app.repository.adoption_repository import AdopcionRepository

class AdopcionService:
    def __init__(self):
        self.repo = AdopcionRepository()

    def create(self, adopcion):
        adopcion.fecha_adopcion = str(datetime.now())

        # regla de negocio: mascota adoptada
        return self.repo.create(adopcion)
    
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