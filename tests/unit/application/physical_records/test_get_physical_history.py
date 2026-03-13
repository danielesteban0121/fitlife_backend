from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.application.use_cases.physical_records.get_physical_history import GetPhysicalHistory
from src.domain.entities.physical_record import PhysicalRecord


@pytest.mark.asyncio
async def test_get_physical_history_success():
    # Arrange
    repository = MagicMock()
    repository.find_by_user_id = AsyncMock()
    use_case = GetPhysicalHistory(repository)
    
    user_id = uuid4()
    records = [
        PhysicalRecord(id=uuid4(), user_id=user_id, weight_kg=80.0, height_cm=180.0),
        PhysicalRecord(id=uuid4(), user_id=user_id, weight_kg=78.0, height_cm=180.0),
    ]
    repository.find_by_user_id.return_value = records

    # Act
    result = await use_case.execute(user_id)

    # Assert
    assert len(result) == 2
    assert result[0].weight_kg == 80.0
    assert result[1].weight_kg == 78.0
    repository.find_by_user_id.assert_called_once_with(user_id)
