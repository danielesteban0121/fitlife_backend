from src.domain.services.password_validator import PasswordValidator


def test_password_validator_valid():
    assert PasswordValidator.validate("SecurePass123")


def test_password_validator_invalid():
    assert not PasswordValidator.validate("short")
