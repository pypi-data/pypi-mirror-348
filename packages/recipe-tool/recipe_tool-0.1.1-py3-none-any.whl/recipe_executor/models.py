"""
Models for Recipe Executor system.

Defines Pydantic models for file specifications and recipe structures.
"""
from typing import Any, Dict, List, Union

from pydantic import BaseModel


class FileSpec(BaseModel):
    """Represents a single file to be generated.

    Attributes:
        path: Relative path where the file should be written.
        content: The content of the file, which can be a string,
                 a mapping, or a list of mappings for structured outputs.
    """
    path: str
    content: Union[str, Dict[str, Any], List[Dict[str, Any]]]


class RecipeStep(BaseModel):
    """A single step in a recipe.

    Attributes:
        type: The type of the recipe step.
        config: Dictionary containing configuration for the step.
    """
    type: str
    config: Dict[str, Any]


class Recipe(BaseModel):
    """A complete recipe with multiple steps.

    Attributes:
        steps: A list of steps defining the recipe.
    """
    steps: List[RecipeStep]