import json
import asyncio
from pathlib import Path
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fit_tech.app.db.session import AsyncSessionLocal
from fit_tech.app.core.models.ingredient import Ingredient
from fit_tech.app.core.models.exercise import Exercise, MuscleGroup
from fit_tech.app.core.models.recipe import Recipe
from fit_tech.app.core.models.recipe_ingredient import RecipeIngredient

BASE_DIR = Path(__file__).resolve().parent
SEED_DIR = BASE_DIR / "seed_data"

def load_json(filename: str):
    path = SEED_DIR / filename
    with open(path, encoding="utf-8") as f:
        return json.load(f)

async def seed_ingredients(session: AsyncSession):
    data = load_json("ingredients.json")
    for item in data:
        exists = await session.execute(
            select(Ingredient).where(Ingredient.name == item["name"])
        )
        if not exists.scalars().first():
            session.add(Ingredient(**item))
    await session.commit()

async def seed_exercises(session: AsyncSession):
    data = load_json("exercises.json")
    for item in data:
        exists = await session.execute(
            select(Exercise).where(Exercise.name == item["name"])
        )
        if not exists.scalars().first():
            item["muscle_group"] = MuscleGroup[item["muscle_group"]]
            session.add(Exercise(**item))
    await session.commit()

async def seed_recipes(session: AsyncSession):
    data_path = Path(__file__).parent / "seed_data" / "recipes.json"
    with data_path.open(encoding="utf-8") as f:
        recipes = json.load(f)

    for item in recipes:
        ingredients_data = item.pop("ingredients", [])
        recipe = Recipe(**item)
        for ingr in ingredients_data:
            assoc = RecipeIngredient(
                ingredient_id=ingr["ingredient_id"],
                amount=ingr["amount"],
                unit=ingr["unit"]
            )
            recipe.ingredients.append(assoc)

        session.add(recipe)
    await session.commit()
    await session.close()


async def run_seeds():
    async with AsyncSessionLocal() as session:
        count = await session.execute(select(func.count()).select_from(Recipe))
        if count.scalar_one() == 0:
            try:
                await seed_ingredients(session)
                await seed_exercises(session)
                await seed_recipes(session)
            except IntegrityError:
                await session.rollback()

if __name__ == "__main__":
    asyncio.run(run_seeds())