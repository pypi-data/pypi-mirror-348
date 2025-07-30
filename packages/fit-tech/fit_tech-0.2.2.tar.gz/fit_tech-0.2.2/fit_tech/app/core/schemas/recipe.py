from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

from fit_tech.app.core.models.recipe_ingredient import UnitType

class IngredientBase(BaseModel):
    name: str
    description: Optional[str] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    fiber: Optional[float] = None
    sugar: Optional[float] = None
    unit: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    is_vegetarian: Optional[bool] = True
    is_vegan: Optional[bool] = False
    is_gluten_free: Optional[bool] = True
    is_dairy_free: Optional[bool] = True

class IngredientCreate(IngredientBase):
    pass

class IngredientInDBBase(IngredientBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class Ingredient(IngredientInDBBase):
    pass

class RecipeIngredientBase(BaseModel):
    ingredient_id: int
    amount: float
    unit: UnitType

class RecipeIngredientCreate(RecipeIngredientBase):
    pass

class RecipeIngredientInDBBase(RecipeIngredientBase):
    id: int
    recipe_id: int
    model_config = ConfigDict(from_attributes=True)

class RecipeIngredient(RecipeIngredientInDBBase):
    ingredient: Optional[Ingredient] = None

class RecipeBase(BaseModel):
    name: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    cook_time: Optional[int] = None
    servings: Optional[int] = 1
    calories: Optional[float] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None

class RecipeCreate(RecipeBase):
    ingredients: List[RecipeIngredientCreate] = []

class RecipeInDBBase(RecipeBase):
    id: int
    user_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

class Recipe(RecipeInDBBase):
    ingredients: List[RecipeIngredient] = Field(default=[], alias="ingredients")

