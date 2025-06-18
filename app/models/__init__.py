# Import all models to ensure they are registered with SQLAlchemy
from .base_models import Faculty, Student, Classes, StudentClass

__all__ = [
    "Faculty",
    "Student", 
    "Classes",
    "StudentClass"
]
