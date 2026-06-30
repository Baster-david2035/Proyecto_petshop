from app.repository.client_repository import ClienteRepository


class ClienteService:
    def __init__(self):
        self.repo = ClienteRepository()

    def create(self, cliente):
        if self.repo.existe(cliente.id_cliente):
            raise ValueError("Cliente ya existe")
        return self.repo.agregar(cliente)

    def get_all(self):
        return self.repo.obtener_todos()

    def get(self, id_cliente):
        return self.repo.buscar_por_id(id_cliente)

    def delete(self, id_cliente):
        return self.repo.eliminar(id_cliente)
