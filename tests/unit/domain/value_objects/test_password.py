import pytest
from src.domain.value_objects.password import Password
from src.domain.exceptions.validation_exceptions import WeakPasswordException


def test_valid_password():
    Password("SecurePass123!")


def test_short_password():
    with pytest.raises(WeakPasswordException):
        Password("Short1!")


def test_missing_uppercase():
    with pytest.raises(WeakPasswordException):
        Password("securepass123!")
