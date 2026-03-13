"""Caso de uso: Cambio de contraseña del usuario autenticado."""
from uuid import UUID

from src.application.dtos.auth_dtos import ChangePasswordRequest, MessageResponse
from src.domain.exceptions.user_exceptions import InvalidCredentials
from src.domain.repositories.user_repository import UserRepository
from src.domain.services.password_hasher import PasswordHasher
from src.domain.services.password_validator import PasswordValidator


class ChangePassword:
    """
    Permite a un usuario autenticado cambiar su contraseña.

    Valida:
    1. Que la contraseña actual sea correcta.
    2. Que la nueva contraseña cumpla las políticas de seguridad.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.password_validator = PasswordValidator()

    async def execute(
        self, user_id: UUID, request: ChangePasswordRequest
    ) -> MessageResponse:
        # 1. Obtener usuario
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise InvalidCredentials("Usuario no encontrado")

        # 2. Verificar contraseña actual
        if not self.password_hasher.verify(request.current_password, user.password_hash):
            raise InvalidCredentials("La contraseña actual es incorrecta")

        # 3. Validar política de la nueva contraseña
        if not self.password_validator.validate(request.new_password):
            from src.domain.exceptions.validation_exceptions import InvalidValueException
            raise InvalidValueException("La nueva contraseña no cumple con las políticas de seguridad (mínimo 8 caracteres, mayúscula, minúscula y número)")


        # 4. Hashear y actualizar
        user.password_hash = self.password_hasher.hash(request.new_password)
        await self.user_repository.save(user)

        return MessageResponse(message="Contraseña actualizada correctamente")
