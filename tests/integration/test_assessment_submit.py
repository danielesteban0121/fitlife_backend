import pytest


@pytest.mark.asyncio
async def test_submit_assessment(client):

    payload = {
        "user_id": 1,
        "answers": [
            {"question_id": 1, "answer": 5},
            {"question_id": 2, "answer": 4},
            {"question_id": 3, "answer": 3},
        ],
    }

    response = await client.post(
        "/api/assessments/submit",
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    assert "fitness_score" in data
