import pytest
from src.domain.value_objects.email import Email
from src.domain.exceptions.validation_exceptions import InvalidEmailException

def test_email_valid():
    email = Email("user@example.com")
    assert str(email) == "user@example.com"

def test_email_invalid():
    with pytest.raises(InvalidEmailException):
        Email("invalid-email")