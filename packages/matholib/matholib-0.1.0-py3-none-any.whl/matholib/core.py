def math_add(numbers):
    """Add a list of numbers"""
    if not isinstance(numbers, (list, tuple)):
        raise TypeError("Input must be a type of list or tuple")
    return sum(numbers)
