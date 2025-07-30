from typing import List, Optional
from fit_tech.app.core.models.recipe import Recipe
from fit_tech.app.core.models.recipe_ingredient import RecipeIngredient
from fit_tech.app.core.schemas.recipe import RecipeCreate
from fit_tech.app.db.repositories.recipe import RecipeRepository
from fit_tech.app.core.services.base import BaseService

class RecipeService(BaseService[Recipe, RecipeCreate]):
    def __init__(self, repository: RecipeRepository):
        super().__init__(repository)
        self.repository = repository
    
    async def get_with_ingredients(self, id: int) -> Optional[Recipe]:
        return await self.repository.get_with_ingredients(id=id)
    
    async def get_multi_by_user(
        self, *, user_id: int, skip: int = 0, limit: int = 100, 
        search: Optional[str] = None,
        max_calories: Optional[int] = None, min_protein: Optional[float] = None
    ) -> List[Recipe]:
        return await self.repository.get_multi_by_user(
            user_id=user_id, skip=skip, limit=limit, 
            search=search, max_calories=max_calories, min_protein=min_protein
        )
    
    async def create_with_ingredients(self, *, recipe_in: RecipeCreate, user_id: int) -> Recipe:
        data = recipe_in.dict(exclude={"ingredients"})
        data["user_id"] = user_id

        recipe = Recipe(**data)
        self.repository.db.add(recipe)
        await self.repository.db.commit()
        await self.repository.db.refresh(recipe)

        for ingredient in recipe_in.ingredients:
            recipe_ingredient = RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient.ingredient_id,
                **ingredient.dict(exclude={"ingredient_id"})
            )
            self.repository.db.add(recipe_ingredient)
        
        await self.repository.db.commit()
        return await self.repository.get_with_ingredients(id=recipe.id)