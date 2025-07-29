class UnitMasterError(Exception):
    """Base exception for the UnitMaster package."""
    pass


class UnitNotFoundError(UnitMasterError):
    """Raised when a specified unit is not found."""
    def __init__(self, unit, category=None):
        self.unit = unit
        self.category = category
        if category:
            message = f"Unit '{unit}' not found in category '{category}'."
        else:
            message = f"Unit '{unit}' not found."
        super().__init__(message)


class CategoryNotFoundError(UnitMasterError):
    """Raised when a specified category is not found."""
    def __init__(self, category):
        self.category = category
        message = f"Category '{category}' not found."
        super().__init__(message)