from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from fit_tech.app.core.models.recipe import Recipe
from fit_tech.app.core.schemas.recipe import Recipe, RecipeCreate
from fit_tech.app.core.services.recipe import RecipeService
from fit_tech.app.api.dependencies import get_recipe_service, CurrentUser

router = APIRouter()

@router.get("/", response_model=List[Recipe])
async def get_recipes(
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None),
    max_calories: Optional[int] = None,
    min_protein: Optional[float] = None,
    recipe_service: RecipeService = Depends(get_recipe_service)
):
    """
    Получить список всех рецептов с фильтрацией
    """
    recipes = await recipe_service.get_multi_by_user(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        search=search,
        max_calories=max_calories,
        min_protein=min_protein
    )
    return recipes

@router.get("/{recipe_id}", response_model=Recipe)
async def get_recipe(
    current_user: CurrentUser,
    recipe_id: int,
    recipe_service: RecipeService = Depends(get_recipe_service)
) -> Recipe:
    """
    Получить детали конкретного рецепта
    """
    recipe = await recipe_service.get_with_ingredients(id=recipe_id)
    if not recipe or (recipe.user_id is not None and recipe.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    return recipe

@router.post("/", response_model=Recipe, status_code=status.HTTP_201_CREATED)
async def create_recipe(
    current_user: CurrentUser,
    recipe_in: RecipeCreate,
    recipe_service: RecipeService = Depends(get_recipe_service)
):
    """
    Создать новый рецепт (только для авторизованных пользователей)
    """
    recipe_data = recipe_in.dict()
    recipe_data["user_id"] = current_user.id

    recipe = await recipe_service.create_with_ingredients(recipe_in=recipe_in, user_id=current_user.id)
    return recipe

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(
    current_user: CurrentUser,
    recipe_id: int,
    recipe_service: RecipeService = Depends(get_recipe_service)
):
    """
    Удалить рецепт (только владелец)
    """
    recipe = await recipe_service.get(id=recipe_id)
    if not recipe or recipe.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found or not owned by user"
        )
    await recipe_service.delete(id=recipe_id)
    return None
