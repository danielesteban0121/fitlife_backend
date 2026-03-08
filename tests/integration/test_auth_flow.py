import uuid

import pytest
from httpx import AsyncClient

from src.main import app


@pytest.mark.asyncio
async def test_register_login_refresh_flow():
    email = f"{uuid.uuid4()}@test.com"

    async with AsyncClient(app=app, base_url="http://test") as client:

        # -------------------------
        # Register
        # -------------------------

        register_response = await client.post(
            "/api/auth/register",
            json={
                "email": email,
                "password": "StrongPass123",
            },
        )

        print(register_response.json())
        assert register_response.status_code == 200

        register_data = register_response.json()

        assert "access_token" in register_data
        assert "refresh_token" in register_data

        refresh_token = register_data["refresh_token"]

        # -------------------------
        # Login
        # -------------------------

        login_response = await client.post(
            "/api/auth/login",
            json={
                "email": email,
                "password": "StrongPass123",
            },
        )

        assert login_response.status_code == 200

        login_data = login_response.json()

        assert "access_token" in login_data
        assert "refresh_token" in login_data

        # -------------------------
        # Refresh
        # -------------------------

        refresh_response = await client.post(
            "/api/auth/refresh",
            json={"token": refresh_token},
        )

        assert refresh_response.status_code == 200

        refresh_data = refresh_response.json()

        assert "access_token" in refresh_data
        assert "refresh_token" in refresh_data
