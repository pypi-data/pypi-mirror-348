from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from fit_tech.app.core.models.base import Base

class MuscleGroup(str, enum.Enum):
    CHEST = "chest"
    BACK = "back"
    LEGS = "legs"
    ARMS = "arms"
    SHOULDERS = "shoulders"
    CORE = "core"
    CARDIO = "cardio"
    OTHER = "other"

class Difficulty(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    muscle_group = Column(Enum(MuscleGroup), nullable=False, index=True)
    difficulty = Column(Enum(Difficulty), nullable=False, index=True)
    equipment = Column(String(255), nullable=True)
    instructions = Column(Text, nullable=True)
    video_url = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    calories_per_hour = Column(Integer, nullable=True)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True) 

    exercises = relationship("WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan")
    author = relationship("User", back_populates="exercises")

    def __repr__(self):
        return f"<Exercise(id={self.id}, name='{self.name}', muscle_group={self.muscle_group})>"

__all__ = ["Exercise", "MuscleGroup", "Difficulty"]