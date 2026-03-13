"""Tests unitarios para PhysicalRecord entity."""
from uuid import uuid4

from src.domain.entities.physical_record import PhysicalRecord


def test_bmi_calculated_correctly():
    record = PhysicalRecord(
        id=uuid4(),
        user_id=uuid4(),
        weight_kg=70.0,
        height_cm=170.0,
    )
    # IMC = 70 / (1.7^2) = 24.22
    assert record.bmi is not None
    assert abs(record.bmi - 24.22) < 0.1


def test_bmi_category_normal():
    record = PhysicalRecord(
        id=uuid4(),
        user_id=uuid4(),
        weight_kg=70.0,
        height_cm=170.0,
    )
    assert record.bmi_category == "Normal"


def test_bmi_category_obese():
    record = PhysicalRecord(
        id=uuid4(),
        user_id=uuid4(),
        weight_kg=120.0,
        height_cm=160.0,
    )
    assert record.bmi_category == "Obese"


def test_bmi_none_when_no_height():
    record = PhysicalRecord(
        id=uuid4(),
        user_id=uuid4(),
        weight_kg=70.0,
        height_cm=0.0,
    )
    assert record.bmi is None
    assert record.bmi_category == "Unknown"


def test_optional_fields_default_none():
    record = PhysicalRecord(
        id=uuid4(),
        user_id=uuid4(),
        weight_kg=65.0,
        height_cm=175.0,
    )
    assert record.body_fat_percentage is None
    assert record.muscle_mass_kg is None
    assert record.waist_cm is None
