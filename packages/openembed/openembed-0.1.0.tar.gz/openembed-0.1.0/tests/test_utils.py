"""Test module for utils.py."""

import pytest
from my_library.utils import is_even, is_prime, factorial


def test_is_even():
    """Test is_even function."""
    assert is_even(2) is True
    assert is_even(4) is True
    assert is_even(0) is True
    assert is_even(1) is False
    assert is_even(7) is False
    assert is_even(-2) is True
    assert is_even(-5) is False


def test_is_prime():
    """Test is_prime function."""
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(5) is True
    assert is_prime(7) is True
    assert is_prime(11) is True
    assert is_prime(13) is True
    
    assert is_prime(1) is False
    assert is_prime(4) is False
    assert is_prime(6) is False
    assert is_prime(8) is False
    assert is_prime(9) is False
    assert is_prime(10) is False
    assert is_prime(12) is False
    assert is_prime(15) is False
    assert is_prime(0) is False
    assert is_prime(-1) is False
    assert is_prime(-5) is False


def test_factorial():
    """Test factorial function."""
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(2) == 2
    assert factorial(3) == 6
    assert factorial(4) == 24
    assert factorial(5) == 120
    
    with pytest.raises(ValueError):
        factorial(-1)