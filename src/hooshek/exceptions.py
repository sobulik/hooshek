class HooshekError(Exception):
    """Base exception for all Hooshek errors."""


class ValidationError(HooshekError):
    """Raised when data validation, schema checking, or duplicate key checks fail."""
