from typing import List, Optional
from fit_tech.app.core.models.ingredient import Ingredient
from fit_tech.app.core.schemas.recipe import IngredientCreate
from fit_tech.app.db.repositories.ingredient import IngredientRepository
from fit_tech.app.core.services.base import BaseService

class IngredientService(BaseService[Ingredient, IngredientCreate]):
    def __init__(self, repository: IngredientRepository):
        super().__init__(repository)
        self.repository = repository
    
    async def get_multi_filtered(
        self, *, 
        skip: int = 0, 
        limit: int = 100, 
        search: Optional[str] = None, 
    ) -> List[Ingredient]:
        return await self.repository.get_multi_filtered(
            skip=skip, 
            limit=limit, 
            search=search
        )
