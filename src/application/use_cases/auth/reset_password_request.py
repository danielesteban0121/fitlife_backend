"""Caso de uso: Solicitar restablecimiento de contraseña (envía email)."""
import secrets

from src.application.dtos.auth_dtos import MessageResponse, ResetPasswordRequestDTO
from src.application.ports.email_service import EmailService
from src.domain.repositories.user_repository import UserRepository
from src.domain.value_objects.email import Email


class ResetPasswordRequest:
    """
    Genera un token de restablecimiento de contraseña y lo envía al email.

    Si el email no existe, responde igual para no revelar registros.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        email_service: EmailService,
    ):
        self.user_repository = user_repository
        self.email_service = email_service

    async def execute(self, dto: ResetPasswordRequestDTO) -> MessageResponse:
        email = Email(dto.email)
        user = await self.user_repository.find_by_email(email)

        # Respuesta genérica para no filtrar si el email existe o no
        if not user:
            return MessageResponse(
                message="Si el email está registrado recibirás un enlace de restablecimiento."
            )

        # Generar token seguro (en producción guardar en BD con expiración)
        reset_token = secrets.token_urlsafe(32)

        # Enviar email con el enlace de restablecimiento
        await self.email_service.send_email(
            to=str(email),
            subject="Restablecimiento de Contraseña - FitLife",
            body=(
                f"Hola,\n\nHaz clic en el siguiente enlace para restablecer tu contraseña:\n"
                f"http://localhost:4200/reset-password?token={reset_token}\n\n"
                f"Este enlace expirará en 1 hora.\n\nEquipo FitLife"
            ),
        )

        return MessageResponse(
            message="Si el email está registrado recibirás un enlace de restablecimiento."
        )
