import uuid
from typing import Dict
from datetime import datetime
from uuid import UUID

from src.domain.entities.message import Message, MessageType
from src.domain.repositories.message_repository import MessageRepository
from src.application.ports.email_service import EmailService


class NotificationService:
    def __init__(self, message_repository: MessageRepository, email_service: EmailService = None):
        self.message_repository = message_repository
        self.email_service = email_service

    async def send_assignment_notification(
        self, user_id: UUID, assignment_type: str, details: Dict
    ) -> None:
        content = f"Se te ha asignado un nuevo {assignment_type}. Detalles: {details}"

        message = Message(
            id=uuid.uuid4(),
            sender_id=None,  # Sistema
            recipient_id=user_id,
            content=content,
            message_type=MessageType.SYSTEM_NOTIFICATION,
            created_at=datetime.utcnow(),
        )
        await self.message_repository.save(message)

        # Enviar por email si el servicio está configurado
        if self.email_service:
            # En un entorno real, buscar usuario en base de datos para obtener su email.
            # Aquí como ejemplo directo asumimos que `email_service` enviará el aviso genérico
            # o implementamos un hook extra para resolver el email.
            try:
                # Mock resolution
                # Requires fetching User entity to get the real email
                to_email = "resolved_user@example.com"
                await self.email_service.send_email(
                    to=to_email, subject=f"Nuevo {assignment_type} asignado - FitLife", body=content
                )
            except Exception as e:
                # Log error in production
                print(f"Failed to send email notification: {e}")
