from tests.calculator import add, subtract, multiply, divide
import pytest

# Basic tests
def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-2, -3) == -5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

# Reusable data
@pytest.fixture
def integer_numbers():
    return 20, 5


def test_divide_integers(integer_numbers):
    a, b = integer_numbers
    assert divide(a, b) == 4


# Parametrization and markers
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
    (2.5, 2.5, 5.0)
])

def test_add_multiple(a, b, expected):
    assert add(a, b) == expected


# Test filtering
@pytest.mark.smoke
def test_add_smoke():
    assert add(5, 5) == 10

@pytest.mark.exception
def test_divide_by_zero_exception():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

# Precision tests
@pytest.fixture
def decimal_numbers():
    return 0.1, 0.2
def test_multiply_precise(decimal_numbers):
    a, b = decimal_numbers
    result = multiply(a, b)
    assert result == pytest.approx(0.02, abs=1e-8)

def test_divide_precise():
    result = divide(1, 3)
    assert result == pytest.approx(0.333333, rel=1e-4)


