from .base import DomainException


class InvalidEmailException(DomainException):
    pass


class WeakPasswordException(DomainException):
    pass


class InvalidBMIException(DomainException):
    pass
