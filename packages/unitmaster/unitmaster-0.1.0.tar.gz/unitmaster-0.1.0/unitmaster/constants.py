CONVERSION_FACTORS = {
    'length': {
        'mm': 0.001,
        'cm': 0.01,
        'm': 1.0,
        'km': 1000.0,
        'in': 0.0254,
        'ft': 0.3048,
        'yd': 0.9144,
        'mi': 1609.344
    },
    'weight': {
        'mg': 0.000001,
        'g': 0.001,
        'kg': 1.0,
        'ton': 1000.0,
        'oz': 0.02834952,
        'lb': 0.45359237
    },
    'volume': {
        'ml': 0.001,
        'l': 1.0,
        'gal': 3.78541,
        'qt': 0.946353,
        'pt': 0.473176,
        'fl_oz': 0.0295735
    },
    'temperature': {
        # Special case - handled with custom conversions
        'c': 0,
        'f': 1,
        'k': 2
    },
    'time': {
        'sec': 1.0,
        'min': 60.0,
        'hr': 3600.0,
        'day': 86400.0,
        'week': 604800.0,
        'month': 2592000.0,  # 30-day month
        'year': 31536000.0   # 365-day year
    },
    'digital': {
        'b': 1.0,  # byte
        'kb': 1024.0,
        'mb': 1048576.0,
        'gb': 1073741824.0,
        'tb': 1099511627776.0
    },
    'area': {
        'mm2': 0.000001,
        'cm2': 0.0001,
        'm2': 1.0,
        'km2': 1000000.0,
        'in2': 0.00064516,
        'ft2': 0.09290304,
        'acre': 4046.8564224,
        'ha': 10000.0  # hectare
    }
}

UNIT_ALIASES = {
    'millimeter': 'mm',
    'millimeters': 'mm',
    'centimeter': 'cm',
    'centimeters': 'cm',
    'meter': 'm',
    'meters': 'm',
    'kilometer': 'km',
    'kilometers': 'km',
    'inch': 'in',
    'inches': 'in',
    'foot': 'ft',
    'feet': 'ft',
    'yard': 'yd',
    'yards': 'yd',
    'mile': 'mi',
    'miles': 'mi',
    
    'milligram': 'mg',
    'milligrams': 'mg',
    'gram': 'g',
    'grams': 'g',
    'kilogram': 'kg',
    'kilograms': 'kg',
    'ounce': 'oz',
    'ounces': 'oz',
    'pound': 'lb',
    'pounds': 'lb',
    
    'milliliter': 'ml',
    'milliliters': 'ml',
    'liter': 'l',
    'liters': 'l',
    'gallon': 'gal',
    'gallons': 'gal',
    'quart': 'qt',
    'quarts': 'qt',
    'pint': 'pt',
    'pints': 'pt',
    'fluid_ounce': 'fl_oz',
    'fluid_ounces': 'fl_oz',
    
    'celsius': 'c',
    'fahrenheit': 'f',
    'kelvin': 'k',
    
    'second': 'sec',
    'seconds': 'sec',
    'minute': 'min',
    'minutes': 'min',
    'hour': 'hr',
    'hours': 'hr',
    'days': 'day',
    'weeks': 'week',
    'months': 'month',
    'years': 'year',
    
    'byte': 'b',
    'bytes': 'b',
    'kilobyte': 'kb',
    'kilobytes': 'kb',
    'megabyte': 'mb',
    'megabytes': 'mb',
    'gigabyte': 'gb',
    'gigabytes': 'gb',
    'terabyte': 'tb',
    'terabytes': 'tb',
    
    'square_millimeter': 'mm2',
    'square_millimeters': 'mm2',
    'square_centimeter': 'cm2',
    'square_centimeters': 'cm2',
    'square_meter': 'm2',
    'square_meters': 'm2',
    'square_kilometer': 'km2',
    'square_kilometers': 'km2',
    'square_inch': 'in2',
    'square_inches': 'in2',
    'square_foot': 'ft2',
    'square_feet': 'ft2',
    'acres': 'acre',
    'hectare': 'ha',
    'hectares': 'ha'
}