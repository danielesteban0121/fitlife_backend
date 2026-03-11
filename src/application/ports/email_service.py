from abc import ABC, abstractmethod

class EmailService(ABC):
    """Puerto de salida para el envío de correos electrónicos."""

    @abstractmethod
    async def send_email(self, to: str, subject: str, body: str) -> bool:
        pass
