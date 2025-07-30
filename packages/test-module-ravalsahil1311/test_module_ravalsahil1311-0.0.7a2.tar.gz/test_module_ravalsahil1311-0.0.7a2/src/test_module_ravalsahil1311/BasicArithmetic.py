def add_Numbers(number1: int, number2: int) -> int:
    """
    This Function will add up the numbers you provide.

    ## Args:
        - number1 (int): the first integer to add.
        - number2 (int): the second integer to add.

    ## Returns:
        - int: the result of addition.
    """
    print(number1 + number2)
    return number1 + number2


def subtract_Numbers(number1: int, number2: int) -> int:
    """
    This Function will subtract the second number from the first.

    ## Args:
        - number1 (int): the number to subtract from.
        - number2 (int): the number to subtract.

    ## Returns:
        - int: the result of subtraction.
    """
    print(number1 - number2)
    return number1 - number2


def multiply_Numbers(number1: int, number2: int) -> int:
    """
    This Function will multiply the numbers you provide.

    ## Args:
        - number1 (int): the first number to multiply.
        - number2 (int): the second number to multiply.

    ## Returns:
        - int: the result of multiplication.
    """
    print(number1 * number2)
    return number1 * number2


def divide_Numbers(number1: int, number2: int) -> float:
    """
    This Function will divide the first number by the second.

    ## Args:
        - number1 (int): the dividend.
        - number2 (int): the divisor.

    ## Returns:
        - float: the result of division.
    """
    if number2 == 0:
        raise ValueError("Division by zero is not allowed.")
    print(number1 / number2)
    return number1 / number2


def modulo_Numbers(number1: int, number2: int) -> int:
    """
    This Function will return the remainder when the first number is divided by the second.

    ## Args:
        - number1 (int): the dividend.
        - number2 (int): the divisor.

    ## Returns:
        - int: the remainder of the division.
    """
    print(number1 % number2)
    return number1 % number2


def power_Numbers(number1: int, number2: int) -> int:
    """
    This Function will raise the first number to the power of the second.

    ## Args:
        - number1 (int): the base number.
        - number2 (int): the exponent.

    ## Returns:
        - int: the result of exponentiation.
    """
    print(number1**number2)
    return number1**number2


def average_Numbers(number1: int, number2: int) -> float:
    """
    This Function will return the average of two numbers.

    ## Args:
        - number1 (int): the first number.
        - number2 (int): the second number.

    ## Returns:
        - float: the average of the two numbers.
    """
    return (number1 + number2) / 2


def gcd_Numbers(number1: int, number2: int) -> int:
    """
    This Function will return the greatest common divisor (GCD) of two numbers.

    ## Args:
        - number1 (int): the first number.
        - number2 (int): the second number.

    ## Returns:
        - int: the greatest common divisor of the two numbers.
    """
    import math

    if number1 < 0 or number2 < 0:
        raise ValueError("GCD is not defined for negative numbers.")

    if number1 == 0 or number2 == 0:
        raise ValueError("GCD is not defined for zero and zero.")

    return math.gcd(number1, number2)


__all__ = [
    "add_Numbers",
    "subtract_Numbers",
    "multiply_Numbers",
    "divide_Numbers",
    "modulo_Numbers",
    "power_Numbers",
    "average_Numbers",
    "gcd_Numbers",
]
