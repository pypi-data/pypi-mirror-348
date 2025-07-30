"""Test module for core.py."""

import pytest
from my_library.core import Calculator


def test_calculator_init():
    """Test calculator initialization."""
    calc = Calculator()
    assert calc.value == 0
    
    calc = Calculator(10)
    assert calc.value == 10


def test_calculator_add():
    """Test calculator add method."""
    calc = Calculator(5)
    assert calc.add(3) == 8
    assert calc.value == 8


def test_calculator_subtract():
    """Test calculator subtract method."""
    calc = Calculator(10)
    assert calc.subtract(4) == 6
    assert calc.value == 6


def test_calculator_multiply():
    """Test calculator multiply method."""
    calc = Calculator(3)
    assert calc.multiply(4) == 12
    assert calc.value == 12


def test_calculator_divide():
    """Test calculator divide method."""
    calc = Calculator(12)
    assert calc.divide(4) == 3
    assert calc.value == 3


def test_calculator_divide_by_zero():
    """Test calculator divide by zero raises error."""
    calc = Calculator(5)
    with pytest.raises(ValueError):
        calc.divide(0)


def test_calculator_reset():
    """Test calculator reset method."""
    calc = Calculator(10)
    assert calc.reset() == 0
    assert calc.value == 0