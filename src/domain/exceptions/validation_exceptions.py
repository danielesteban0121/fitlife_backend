from .base import DomainException


class InvalidEmailException(DomainException):
    pass


class WeakPasswordException(DomainException):
    pass


class InvalidBMIException(DomainException):
    pass


class InvalidValueException(DomainException):
    """Excepción para valores fuera de rango o inválidos en value objects."""
    pass
