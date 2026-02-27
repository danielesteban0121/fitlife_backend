from pydantic import BaseModel, EmailStr, Field


class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class RegisterUserResponse(BaseModel):
    user_id: str
    email: EmailStr
    access_token: str
    expires_in: int
