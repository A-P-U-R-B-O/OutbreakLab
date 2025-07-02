import pytest
from src.utils import validate_parameters, clamp, to_int, to_float

def test_validate_parameters_valid():
    # Should not raise
    validate_parameters(N=1000, I0=10, R0=0, beta=0.2, gamma=0.1, days=50, dt=1.0)
    validate_parameters(N=100, I0=0, R0=0, beta=0.0, gamma=0.0, days=1, dt=0.5)

@pytest.mark.parametrize("params", [
    {"N": -1, "I0": 1, "R0": 0, "beta":0.3, "gamma":0.1, "days":10, "dt":1.0},
    {"N": 10, "I0": 11, "R0": 0, "beta":0.3, "gamma":0.1, "days":10, "dt":1.0},
    {"N": 10, "I0": 5, "R0": 6, "beta":0.3, "gamma":0.1, "days":10, "dt":1.0},
    {"N": 10, "I0": 5, "R0": 5, "beta":1.2, "gamma":0.1, "days":10, "dt":1.0},
    {"N": 10, "I0": 5, "R0": 5, "beta":0.3, "gamma":-0.1, "days":10, "dt":1.0},
    {"N": 10, "I0": 5, "R0": 5, "beta":0.3, "gamma":0.1, "days":0, "dt":1.0},
    {"N": 10, "I0": 5, "R0": 5, "beta":0.3, "gamma":0.1, "days":10, "dt":-1.0},
])
def test_validate_parameters_invalid(params):
    with pytest.raises(AssertionError):
        validate_parameters(**params)

def test_clamp():
    assert clamp(5, 0, 10) == 5
    assert clamp(-1, 0, 10) == 0
    assert clamp(11, 0, 10) == 10

def test_to_int():
    assert to_int("5") == 5
    assert to_int(7.2) == 7
    assert to_int("not_a_number", default=42) == 42

def test_to_float():
    assert to_float("2.5") == 2.5
    assert to_float(7) == 7.0
    assert to_float("bad", default=3.14) == 3.14
