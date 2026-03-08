import pytest
from httpx import AsyncClient
import uuid
from src.main import app


@pytest.mark.asyncio
async def test_assessment_flow():
    email = f"{uuid.uuid4()}@test.com"
    password = "StrongPassword123"

    async with AsyncClient(app=app, base_url="http://test") as client:
        # 1. Register
        register_response = await client.post(
            "/api/auth/register",
            json={"email": email, "password": password},
        )
        assert register_response.status_code == 200

        # 2. Login
        login_response = await client.post(
            "/api/auth/login",
            json={"email": email, "password": password},
        )
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        # 3. Submit Assessment
        headers = {"Authorization": f"Bearer {access_token}"}

        assessment_payload = {
            "goal": "endurance",
            "activity_level": "very_active",
            "experience_level": "advanced",
            "height_cm": 180.0,
            "weight_kg": 75.0,
            "age": 30,
        }

        assessment_response = await client.post(
            "/api/assessments/submit",
            json=assessment_payload,
            headers=headers,
        )

        assert assessment_response.status_code == 200
        data = assessment_response.json()

        assert "id" in data
        assert "user_id" in data
        assert "fitness_score" in data
        assert data["goal"] == "endurance"
        assert data["fitness_score"] > 0
