from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import or_

from fit_tech.app.core.models.ingredient import Ingredient
from fit_tech.app.core.schemas.recipe import IngredientCreate
from fit_tech.app.db.repositories.base import BaseRepository

class IngredientRepository(BaseRepository[Ingredient, IngredientCreate]):
    def __init__(self, db: Session):
        super().__init__(Ingredient, db)

    async def get_multi_filtered(
        self, *, 
        skip: int = 0, 
        limit: int = 100, 
        search: Optional[str] = None
    ) -> List[Ingredient]:
        query = select(self.model)
        
            
        if search:
            query = query.where(
                or_(
                    self.model.name.ilike(f"%{search}%"),
                    self.model.description.ilike(f"%{search}%")
                )
            )
            
        query = query.order_by(self.model.name).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()