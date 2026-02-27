from src.infrastructure.security.bcrypt_password_hasher import BCryptPasswordHasher


def test_hash_returns_different_value():
    hasher = BCryptPasswordHasher()
    password = "mysecret"

    hashed = hasher.hash(password)

    assert hashed != password
    assert isinstance(hashed, str)


def test_verify_returns_true_for_valid_password():
    hasher = BCryptPasswordHasher()
    password = "mysecret"

    hashed = hasher.hash(password)

    assert hasher.verify(password, hashed) is True


def test_verify_returns_false_for_invalid_password():
    hasher = BCryptPasswordHasher()
    password = "mysecret"

    hashed = hasher.hash(password)

    assert hasher.verify("wrongpassword", hashed) is False
