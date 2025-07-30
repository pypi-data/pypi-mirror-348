from operator import or_
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload

from fit_tech.app.core.models.recipe import Recipe
from fit_tech.app.core.models.recipe_ingredient import RecipeIngredient
from fit_tech.app.core.schemas.recipe import RecipeCreate
from fit_tech.app.db.repositories.base import BaseRepository


class RecipeRepository(BaseRepository[Recipe, RecipeCreate]):
    def __init__(self, db: Session):
        super().__init__(Recipe, db)

    async def get_with_ingredients(self, id: int) -> Optional[Recipe]:
        query = (select(Recipe).options(
                selectinload(Recipe.ingredients).selectinload(
                    RecipeIngredient.ingredient
                )
            ).where(Recipe.id == id)
        )
        result = await self.db.execute(query)
        recipe = result.scalars().first()
        return recipe

    async def get_multi_by_user(
        self, *, user_id: int, skip: int = 0, limit: int = 100,
        search: Optional[str] = None, max_calories: Optional[int] = None, min_protein: Optional[float] = None
    ) -> List[Recipe]:
        query = select(Recipe).where(or_(Recipe.user_id == user_id, Recipe.user_id.is_(None))).options(
            selectinload(Recipe.ingredients).selectinload(
                RecipeIngredient.ingredient
            )
        )
        if search:
            pattern = f"%{search}%"
            query = query.where(Recipe.name.ilike(pattern))

        if max_calories is not None:
            query = query.where(self.model.calories <= max_calories)
        if min_protein is not None:
            query = query.where(self.model.protein >= min_protein)

        query = query.order_by(self.model.name).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

