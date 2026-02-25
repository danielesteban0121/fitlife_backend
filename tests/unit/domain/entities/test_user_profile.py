from uuid import uuid4
from datetime import date
from src.domain.entities.user_profile import UserProfile


def test_user_profile_creation():
    profile = UserProfile(
        id=uuid4(),
        user_id=uuid4(),
        full_name="Prueba TEST_User_profile",
        date_of_birth=date(2000, 1, 1),
        height_cm=175,
    )

    assert profile.full_name == "Prueba TEST_User_profile"
