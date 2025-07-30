from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.orm import relationship

from fit_tech.app.core.models.base import Base

class Recipe(Base):
    """
    Модель для хранения информации о рецептах.
    Содержит данные о названии, описании, времени приготовления, калорийности и других характеристиках рецепта.
    """
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=False)
    cook_time = Column(Integer, nullable=True)
    servings = Column(Integer, nullable=False, default=1)
    calories = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)
    carbs = Column(Float, nullable=True)
    fat = Column(Float, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
    user = relationship("User", back_populates="recipes")

    def __repr__(self):
        return f"<Recipe(id={self.id}, name='{self.name}', calories={self.calories})>"