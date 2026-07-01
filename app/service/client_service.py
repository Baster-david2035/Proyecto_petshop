from app.repository.client_repository import ClienteRepository


class ClienteService:
    def __init__(self):
        self.repo = ClienteRepository()

    def create(self, cliente):
        if self.repo.exist(cliente.id_cliente):
            raise ValueError("Cliente ya existe")
        return self.repo.create(cliente)

    def get_all(self):
        return self.repo.get_all()

    def get(self, id_cliente):
        return self.repo.get(id_cliente)

    def delete(self, id_cliente):
        return self.repo.delete(id_cliente)
