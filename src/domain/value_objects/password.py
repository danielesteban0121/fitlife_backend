import re
from dataclasses import dataclass

from ..exceptions.validation_exceptions import WeakPasswordException


@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if len(self.value) < 8:
            raise WeakPasswordException("Debe tener mínimo 8 caracteres")

        if not re.search(r"[A-Z]", self.value):
            raise WeakPasswordException("Debe contener una mayúscula")

        if not re.search(r"[a-z]", self.value):
            raise WeakPasswordException("Debe contener una minúscula")

        if not re.search(r"[0-9]", self.value):
            raise WeakPasswordException("Debe contener un número")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", self.value):
            raise WeakPasswordException("Debe contener un carácter especial")
