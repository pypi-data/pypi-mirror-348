"""
Utility functions for the library.
This module contains helper functions used throughout the library.
"""

def is_even(number):
    """Check if a number is even.
    
    Args:
        number (int): The number to check.
        
    Returns:
        bool: True if the number is even, False otherwise.
    """
    return number % 2 == 0

def is_prime(number):
    """Check if a number is prime.
    
    Args:
        number (int): The number to check.
        
    Returns:
        bool: True if the number is prime, False otherwise.
    """
    if number <= 1:
        return False
    if number <= 3:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False
    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6
    return True

def factorial(number):
    """Calculate the factorial of a number.
    
    Args:
        number (int): The number to calculate factorial for.
        
    Returns:
        int: The factorial of the number.
        
    Raises:
        ValueError: If number is negative.
    """
    if number < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if number == 0 or number == 1:
        return 1
    result = 1
    for i in range(2, number + 1):
        result *= i
    return result