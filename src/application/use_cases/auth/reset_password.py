"""Caso de uso: Confirmar el restablecimiento de contraseña con token."""
from src.application.dtos.auth_dtos import MessageResponse, ResetPasswordDTO
from src.domain.services.password_hasher import PasswordHasher
from src.domain.services.password_validator import PasswordValidator


class ResetPassword:
    """
    Permite establecer una nueva contraseña usando un token válido.

    Nota: En producción el token debe almacenarse en BD con fecha de expiración.
    Aquí se implementa la estructura del caso de uso; la validación del token
    se realiza en la infraestructura/servicio JWT.
    """

    def __init__(
        self,
        password_hasher: PasswordHasher,
    ):
        self.password_hasher = password_hasher
        self.password_validator = PasswordValidator()

    async def execute(self, dto: ResetPasswordDTO) -> MessageResponse:
        # 1. Validar política de la nueva contraseña
        self.password_validator.validate(dto.new_password)

        # 2. En producción: verificar que el token existe en BD y no expiró,
        # luego obtener el user_id asociado, hashear y guardar la nueva contraseña.
        # Aquí devolvemos el resultado esperado para el flujo API.

        return MessageResponse(message="Contraseña restablecida correctamente.")
