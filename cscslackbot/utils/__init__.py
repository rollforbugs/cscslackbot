def clamp(x, lower, upper):
    """
    Clamps a comparable value to a range. Intended for numbers
    but should work for any type that implements `>` and `<`.

    Args:
        x (T): value to be clamped
        lower (T): min value for x
        upper (T): max value for x

    Returns:
        (T) x clamped.

    """
    return lower if x < lower else upper if x > upper else x
