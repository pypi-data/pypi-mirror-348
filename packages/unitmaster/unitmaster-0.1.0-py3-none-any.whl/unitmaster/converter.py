from unitmaster.constants import CONVERSION_FACTORS, UNIT_ALIASES
from unitmaster.exceptions import UnitNotFoundError, CategoryNotFoundError


def _get_category(unit):
    """
    Find the category for a given unit.
    
    Args:
        unit (str): The unit to find the category for.
        
    Returns:
        str: The category name.
        
    Raises:
        UnitNotFoundError: If the unit is not found in any category.
    """
    # Check if unit is an alias and convert to standard form
    standardized_unit = UNIT_ALIASES.get(unit.lower(), unit.lower())
    
    for category, units in CONVERSION_FACTORS.items():
        if standardized_unit in units:
            return category
    
    raise UnitNotFoundError(unit)


def _convert_temperature(value, from_unit, to_unit):
    """
    Handle temperature conversions - special case.
    
    Args:
        value (float): The value to convert.
        from_unit (str): The unit to convert from.
        to_unit (str): The unit to convert to.
        
    Returns:
        float: The converted value.
    """
    # Standardize units
    from_unit = UNIT_ALIASES.get(from_unit.lower(), from_unit.lower())
    to_unit = UNIT_ALIASES.get(to_unit.lower(), to_unit.lower())
    
    # Convert to Celsius first
    if from_unit == 'c':
        celsius = value
    elif from_unit == 'f':
        celsius = (value - 32) * 5/9
    elif from_unit == 'k':
        celsius = value - 273.15
    else:
        raise UnitNotFoundError(from_unit, 'temperature')
    
    # Convert from Celsius to the target unit
    if to_unit == 'c':
        return celsius
    elif to_unit == 'f':
        return celsius * 9/5 + 32
    elif to_unit == 'k':
        return celsius + 273.15
    else:
        raise UnitNotFoundError(to_unit, 'temperature')


def convert(value, from_unit, to_unit, category=None):
    """
    Convert a value from one unit to another.
    
    Args:
        value (float): The value to convert.
        from_unit (str): The unit to convert from.
        to_unit (str): The unit to convert to.
        category (str, optional): The category of the units. If not provided,
                                 it will be determined automatically.
    
    Returns:
        float: The converted value.
        
    Raises:
        UnitNotFoundError: If the specified unit is not found.
        CategoryNotFoundError: If the specified category is not found.
    """
    # Standardize inputs
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    # Get standard form of units using aliases
    from_unit = UNIT_ALIASES.get(from_unit, from_unit)
    to_unit = UNIT_ALIASES.get(to_unit, to_unit)
    
    # Determine the category if not provided
    if category is None:
        category = _get_category(from_unit)
    else:
        category = category.lower()
        if category not in CONVERSION_FACTORS:
            raise CategoryNotFoundError(category)
    
    # Handle temperature specially
    if category == 'temperature':
        return _convert_temperature(value, from_unit, to_unit)
    
    # Regular conversion
    category_units = CONVERSION_FACTORS.get(category)
    if category_units is None:
        raise CategoryNotFoundError(category)
    
    from_factor = category_units.get(from_unit)
    if from_factor is None:
        raise UnitNotFoundError(from_unit, category)
    
    to_factor = category_units.get(to_unit)
    if to_factor is None:
        raise UnitNotFoundError(to_unit, category)
    
    # Calculate conversion
    return value * from_factor / to_factor


def get_available_categories():
    """
    Get a list of all available unit categories.
    
    Returns:
        list: A list of category names.
    """
    return list(CONVERSION_FACTORS.keys())


def get_available_units(category=None):
    """
    Get a list of all available units, optionally filtered by category.
    
    Args:
        category (str, optional): The category to filter by.
        
    Returns:
        dict or list: A dictionary mapping categories to lists of units,
                     or just a list of units if a category is specified.
                     
    Raises:
        CategoryNotFoundError: If the specified category is not found.
    """
    if category is None:
        # Return all units grouped by category
        result = {}
        for cat, units in CONVERSION_FACTORS.items():
            result[cat] = list(units.keys())
        return result
    
    # Return units for a specific category
    category = category.lower()
    if category not in CONVERSION_FACTORS:
        raise CategoryNotFoundError(category)
    
    return list(CONVERSION_FACTORS[category].keys())