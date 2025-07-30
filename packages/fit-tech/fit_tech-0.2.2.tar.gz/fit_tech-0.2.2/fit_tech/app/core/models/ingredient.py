from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from fit_tech.app.core.models.base import Base

class Ingredient(Base):
    """
    Модель для хранения информации об ингредиентах.
    Содержит данные о названии, пищевой ценности и других характеристиках ингредиента.
    """
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    calories = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)
    carbs = Column(Float, nullable=True)
    fat = Column(Float, nullable=True)
    fiber = Column(Float, nullable=True)
    sugar = Column(Float, nullable=True)
    unit = Column(String(50), nullable=True)
    image_url = Column(String(255), nullable=True)
    category = Column(String(100), nullable=True, index=True)
    is_vegetarian = Column(Boolean, default=True)
    is_vegan = Column(Boolean, default=False)
    is_gluten_free = Column(Boolean, default=True)
    is_dairy_free = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    ingredients = relationship("RecipeIngredient", back_populates="ingredient", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Ingredient(id={self.id}, name='{self.name}', calories={self.calories})>"