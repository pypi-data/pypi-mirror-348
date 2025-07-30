import numbers


def is_numba(var):
    """Determine if the input is a number

    Args:
        var (Any): Variable to test for number-ness

    Returns:
        bool: Is the input var a number? 
    """
    return isinstance(var, numbers.Number)