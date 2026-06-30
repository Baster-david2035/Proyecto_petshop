from app.repository.user_repository import UsuarioRepository

class UsuarioService:
    def __init__(self):
        self.repo = UsuarioRepository()

    def login(self, username, password):
        user = self.repo.get_by_username(username)
        if not user or user.contrasena != password:
            return None
        return user

    def register(self, username, password):
        if self.repo.get_by_username(username):
            raise ValueError("Usuario ya existe")
        return self.repo.create(username, password)