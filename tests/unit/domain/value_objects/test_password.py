import pytest
from src.domain.value_objects.password import Password
from src.domain.exceptions.validation_exceptions import WeakPasswordException


def test_missing_number():
    with pytest.raises(WeakPasswordException):
        Password("SecurePass!")


def test_missing_special():
    with pytest.raises(WeakPasswordException):
        Password("SecurePass123")


def test_missing_lowercase():
    with pytest.raises(WeakPasswordException):
        Password("SECURE123!")