from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.application.dtos.physical_record_dtos import CreatePhysicalRecordRequest
from src.application.use_cases.physical_records.create_physical_record import CreatePhysicalRecord
from src.domain.entities.physical_record import PhysicalRecord


@pytest.mark.asyncio
async def test_create_physical_record_success():
    # Arrange
    repository = MagicMock()
    repository.save = AsyncMock()
    use_case = CreatePhysicalRecord(repository)
    
    user_id = uuid4()
    request = CreatePhysicalRecordRequest(
        weight_kg=75.0,
        height_cm=180.0,
        body_fat_percentage=20.0,
        notes="Prueba de registro"
    )
    
    # Mocking saved object for return
    repository.save.side_effect = lambda r: r

    # Act
    result = await use_case.execute(user_id, request)

    # Assert
    assert result.user_id == user_id
    assert result.weight_kg == 75.0
    assert result.height_cm == 180.0
    assert result.bmi is not None
    assert result.bmi_category == "Normal"
    repository.save.assert_called_once()
    saved_record = repository.save.call_args[0][0]
    assert isinstance(saved_record, PhysicalRecord)
    assert saved_record.user_id == user_id
