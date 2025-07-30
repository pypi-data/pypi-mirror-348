from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from fit_tech.app.core.models.user import User
from fit_tech.app.core.schemas.user import UserCreate
from fit_tech.app.db.repositories.base import BaseRepository
from fit_tech.app.core.security import get_password_hash
from fit_tech.app.core.security import verify_password

class UserRepository(BaseRepository[User, UserCreate]):
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    async def get_by_email(self, *, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()
    
    async def get_by_username(self, *, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        result = await self.db.execute(query)
        return result.scalars().first()
    
    async def create(self, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_active=True,
            is_superuser=obj_in.is_superuser if hasattr(obj_in, "is_superuser") else False
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
    
    async def authenticate(self, *, email: str, password: str) -> Optional[User]:
        """
        Ищем пользователя по email и сверяем пароль.
        Возвращаем User или None.
        """
        user = await self.get_by_email(email=email)
        if user is None:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    async def is_active(self, user: User) -> bool:
        return user.is_active

    async def is_superuser(self, user: User) -> bool:
        return user.is_superuser