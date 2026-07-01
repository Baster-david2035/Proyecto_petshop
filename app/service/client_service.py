from app.repository.client_repository import ClienteRepository
from app.entity.client import ClienteORM


class ClienteService:
    def __init__(self):
        self.repo = ClienteRepository()

    def create(self, cliente_data):
        """Agrega un cliente nuevo. El estado siempre queda 'Activo'."""
        if self.repo.get_by_correo(cliente_data.correo):
            raise ValueError("Ya existe un cliente con ese correo")

        cliente = ClienteORM(
            nombre=cliente_data.nombre,
            telefono=cliente_data.telefono,
            correo=cliente_data.correo,
            estado="Activo",  # Control de usuarios: estado activo siempre
        )
        return self.repo.create(cliente)

    def get_all(self):
        return self.repo.get_all()

    def get(self, id_cliente):
        return self.repo.get(id_cliente)

    def get_by_correo(self, correo):
        return self.repo.get_by_correo(correo)

    def delete(self, id_cliente):
        return self.repo.delete(id_cliente)
