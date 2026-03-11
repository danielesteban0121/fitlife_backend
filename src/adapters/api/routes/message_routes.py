from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID
from src.adapters.api.dependencies import get_current_user
from src.adapters.api.dependencies_phase_f import get_send_message, get_get_messages
from src.application.dtos.message_dtos import (
    SendMessageRequest,
    SendMessageResponse,
    MessageResponse,
)

router = APIRouter(prefix="/api/messages", tags=["Messages"])


@router.post("/", response_model=SendMessageResponse)
async def send_message(
    request: SendMessageRequest,
    use_case=Depends(get_send_message),
    current_user: dict = Depends(get_current_user),
):
    return await use_case.execute(request)


@router.get("/{user_id}", response_model=List[MessageResponse])
async def get_messages(
    user_id: UUID,
    skip: int = 0,
    limit: int = 50,
    use_case=Depends(get_get_messages),
    current_user: dict = Depends(get_current_user),
):
    return await use_case.execute(user_id, skip=skip, limit=limit)
