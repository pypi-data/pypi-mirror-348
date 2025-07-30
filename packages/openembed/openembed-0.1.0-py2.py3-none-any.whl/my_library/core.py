"""
Core functionality for the library.
This module contains the primary features of the library.
"""

class Calculator:
    """A simple calculator class to demonstrate library functionality."""
    
    def __init__(self, initial_value=0):
        """Initialize the calculator with an optional starting value.
        
        Args:
            initial_value (float, optional): The starting value. Defaults to 0.
        """
        self.value = initial_value
    
    def add(self, x):
        """Add a number to the current value.
        
        Args:
            x (float): The number to add.
            
        Returns:
            float: The new value after addition.
        """
        self.value += x
        return self.value
    
    def subtract(self, x):
        """Subtract a number from the current value.
        
        Args:
            x (float): The number to subtract.
            
        Returns:
            float: The new value after subtraction.
        """
        self.value -= x
        return self.value
    
    def multiply(self, x):
        """Multiply the current value by a number.
        
        Args:
            x (float): The number to multiply by.
            
        Returns:
            float: The new value after multiplication.
        """
        self.value *= x
        return self.value
    
    def divide(self, x):
        """Divide the current value by a number.
        
        Args:
            x (float): The number to divide by.
            
        Returns:
            float: The new value after division.
            
        Raises:
            ValueError: If x is zero.
        """
        if x == 0:
            raise ValueError("Division by zero is not allowed")
        self.value /= x
        return self.value
    
    def reset(self):
        """Reset the calculator to zero.
        
        Returns:
            float: The new value (0).
        """
        self.value = 0
        return self.value