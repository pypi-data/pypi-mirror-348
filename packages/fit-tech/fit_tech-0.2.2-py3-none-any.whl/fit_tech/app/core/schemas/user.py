from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    telegram_id: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str = Field(..., min_length=8, error_msg='Пароль должен быть не менее 8 символов')

    @field_validator('email', mode='before')
    @classmethod
    def check_email_format(cls, v):
        if isinstance(v, str):
            parts = v.split('@', 1)
            if len(parts) != 2 or '.' not in parts[1]:
                raise ValueError('Неверный формат email-адреса')
        return v

class UserInDBBase(UserBase):
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None

class TelegramLoginSchema(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str
