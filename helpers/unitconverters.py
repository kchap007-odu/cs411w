def kelvin_to_celsius(value: float = 0) -> float:
    """Converts a value from Kelvin temperature scale to Celsius
    temperature scale.

    Args:
        value (float, optional): The value to convert. Defaults to 0.

    Returns:
        float: The equivalent value in Celsius.
    """
    return value - 273.15


def celsius_to_kelvin(value: float = 0) -> float:
    """Converts a value from Celsius temperature scale to Kelvin
    temperature scale.

    Args:
        value (float, optional): The value to convert. Defaults to 0.

    Returns:
        float: The equivalent value in Kelvin.
    """
    return value + 273.15


def celsius_to_fahrenheit(value: float = 0) -> float:
    """Converts a value from Celsius temperature scale to Fahrenheit
    temperature scale.

    Args:
        value (float, optional): The value to convert. Defaults to 0.

    Returns:
        float: The equivalent value in Fahrenheit.
    """
    return value * (9/5) + 32


def fahrenheit_to_celsius(value: float = 0) -> float:
    """Converts a value from Fahrenheit temperature scale to Celsius
    temperature scale.

    Args:
        value (float, optional): The value to convert. Defaults to 0.

    Returns:
        float: The equivalent value in Celsius.
    """
    return (value - 32) * (5/9)
