from datetime import datetime
from app.repository.adoption_repository import AdopcionRepository

class AdopcionService:
    def __init__(self):
        self.repo = AdopcionRepository()

    def create(self, adopcion):
        adopcion.fecha_adopcion = str(datetime.now())

        # regla de negocio: mascota adoptada
        return self.repo.agregar(adopcion)

    def get_all(self):
        return self.repo.obtener_todos()

    def get_by_client(self, id_cliente):
        return self.repo.obtener_por_cliente(id_cliente)

    def delete(self, id_adopcion):
        return self.repo.eliminar(id_adopcion)

    def ganancias(self):
        return self.repo.obtener_ganancias_totales()