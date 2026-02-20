import re
from dataclasses import dataclass
from ..exceptions.validation_exceptions import InvalidEmailException

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not self._is_valid(self.value):
            raise InvalidEmailException(f"Formato inválido: {self.value}")

    @staticmethod
    def _is_valid(email: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

    def __str__(self) -> str:
        return self.value
# ----Qué estamos logrando aquí

# #Inmutabilidad (frozen=True)

# Validación automática

# Si es inválido → explota en el dominio

# No depende de FastAPI