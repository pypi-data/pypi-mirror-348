from fastapi import APIRouter, Depends, HTTPException, status

from typing import List, Optional

from app.core.models.ingredient import Ingredient
from app.core.services.ingredient import IngredientService
from app.core.schemas.recipe import Ingredient
from app.api.dependencies import get_ingredient_service, CurrentUser

router = APIRouter(tags=["ingredients"])

@router.get("/", response_model=List[Ingredient])
async def get_ingredients(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    ingredient_service: IngredientService = Depends(get_ingredient_service)
):
    """
    Получить список ингредиентов с возможностью поиска
    """
    ingredients = await ingredient_service.get_multi_filtered(
        skip=skip,
        limit=limit,
        search=search
    )
    return ingredients

@router.get("/{ingredient_id}", response_model=Ingredient)
async def get_ingredient(
    ingredient_id: int,
    current_user: CurrentUser,
    ingredient_service: IngredientService = Depends(get_ingredient_service)
):
    """
    Получить детали ингредиента по ID
    """
    ingredient = await ingredient_service.get(id=ingredient_id)
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ингредиент не найден"
        )
    return ingredient
