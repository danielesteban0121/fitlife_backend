import uuid

import pytest


@pytest.mark.asyncio
async def test_submit_assessment(client):
    """
    Test the full assessment submission flow:
    1. Register a new user
    2. Login to get an access token
    3. Submit an assessment (authenticated)
    4. Verify the response contains fitness_score
    """
    email = f"{uuid.uuid4()}@test.com"
    password = "StrongPassword123"

    # 1. Register
    register_response = await client.post(
        "/api/auth/register",
        json={"email": email, "password": password},
    )
    assert register_response.status_code == 200, register_response.text

    # 2. Login
    login_response = await client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert login_response.status_code == 200, login_response.text
    access_token = login_response.json()["access_token"]

    # 3. Submit assessment with valid auth token
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "goal": "muscle_gain",
        "activity_level": "moderately_active",
        "experience_level": "intermediate",
        "height_cm": 175.0,
        "weight_kg": 70.0,
        "age": 25,
    }

    response = await client.post(
        "/api/assessments/submit",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 200, response.text
    data = response.json()

    assert "fitness_score" in data
    assert "id" in data
    assert "user_id" in data
    assert data["goal"] == "muscle_gain"
    assert data["fitness_score"] > 0
