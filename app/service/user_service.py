from app.repository.user_repository import UsuarioRepository
from app.repository.client_repository import ClienteRepository
from app.entity.client import ClienteORM

ADMIN_CORREO = "admin@petshop.com"
ADMIN_PASSWORD = "admin123"


class UsuarioService:
    def __init__(self):
        self.repo = UsuarioRepository()
        self.cliente_repo = ClienteRepository()

    def login(self, correo, contrasena):
        """
        Valida login. Primero revisa si es el admin fijo, luego busca
        el usuario y valida que exista y que la contrasena coincida.
        """
        if correo == ADMIN_CORREO and contrasena == ADMIN_PASSWORD:
            return {
                "mensaje": "Login exitoso",
                "es_admin": True,
                "id_cliente": None,
                "nombre": "Administrador",
                "correo": ADMIN_CORREO,
            }

        user = self.repo.get_by_username(correo)
        if not user or user.contrasena != contrasena:
            return None

        cliente = self.cliente_repo.get(user.id_cliente) if user.id_cliente else None
        return {
            "mensaje": "Login exitoso",
            "es_admin": False,
            "id_cliente": user.id_cliente,
            "nombre": cliente.nombre if cliente else None,
            "correo": user.nombre_usuario,
        }

    def registrar(self, registro_data):
        """
        Registro: guarda el cliente y el usuario al mismo tiempo.
        Valida que no exista ya un correo / usuario registrado.
        """
        if self.cliente_repo.get_by_correo(registro_data.correo):
            raise ValueError("Ya existe un cliente registrado con ese correo")

        if self.repo.get_by_username(registro_data.correo):
            raise ValueError("Ya existe un usuario registrado con ese correo")

        cliente = ClienteORM(
            nombre=registro_data.nombre,
            telefono=registro_data.telefono,
            correo=registro_data.correo,
            estado="Activo",  # Estado activo siempre
        )
        cliente = self.cliente_repo.create(cliente)

        usuario = self.repo.create(
            username=registro_data.correo,
            password=registro_data.contrasena,
            id_cliente=cliente.id_cliente,
        )

        return {
            "mensaje": "Registro exitoso",
            "id_cliente": cliente.id_cliente,
            "nombre_usuario": usuario.nombre_usuario,
        }

    def recuperar_contrasena(self, correo, nueva_contrasena):
        """Recuperar: restaura la contrasena segun el correo (nombre_usuario = correo)."""
        usuario = self.repo.update_password(correo, nueva_contrasena)
        if not usuario:
            raise ValueError("No existe un usuario con ese correo")
        return {"mensaje": "Contrasena actualizada correctamente"}

    def get_all(self):
        return self.repo.get_all()
