import pytest

from src.domain.repositories.user_repository import UserRepository


def test_cannot_instantiate_abstract_repository():
    with pytest.raises(TypeError):
        UserRepository()
