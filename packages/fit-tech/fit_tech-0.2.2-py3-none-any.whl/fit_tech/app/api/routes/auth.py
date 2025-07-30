from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any

from fit_tech.app.core.schemas.user import UserCreate, User, Token, TelegramLoginSchema
from fit_tech.app.core.services.user import UserService
from fit_tech.app.api.dependencies import get_user_service
from fit_tech.app.core.security import verify_telegram_hash, get_current_active_user

router = APIRouter(tags=["auth"])

@router.post("/telegram", response_model=User)
async def link_telegram(
    data: TelegramLoginSchema,
    current_user: User = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service),
):
    verify_telegram_hash(data)
    updated_user = await user_service.link_telegram(
        db_obj=current_user,
        obj_in={"telegram_id": str(data.id)},
    )
    return updated_user

@router.post("/signup", response_model=User)
async def signup(
    user_in: UserCreate, 
    user_service: UserService = Depends(get_user_service)
) -> Any:
    """
    Регистрация нового пользователя
    """
    try:
        user = await user_service.create(obj_in=user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
) -> Any:
    """
    Аутентификация пользователя и получение токена доступа
    """
    user = await user_service.get_by_email(email=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email не найден"
        )

    auth_result = await user_service.authenticate(
        email=form_data.username, 
        password=form_data.password
    )
    
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "access_token": auth_result["access_token"], 
        "token_type": auth_result["token_type"]
    }
