from .base import DomainException


class UserNotFoundException(DomainException):
    pass


class EmailAlreadyExistsException(DomainException):
    pass


class InvalidCredentials(DomainException):
    pass
