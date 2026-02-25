import pytest

from src.domain.exceptions.validation_exceptions import InvalidEmailException
from src.domain.value_objects.email import Email


def test_email_valid():
    email = Email("user@example.com")
    assert str(email) == "user@example.com"


def test_email_invalid():
    with pytest.raises(InvalidEmailException):
        Email("invalid-email")
