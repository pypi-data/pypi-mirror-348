"""
My Library - A simple calculator and math utilities library.

This library provides a calculator class and various math utility functions.
"""

__version__ = '0.1.0'

from .core import Calculator
from .utils import is_even, is_prime, factorial

__all__ = ['Calculator', 'is_even', 'is_prime', 'factorial']