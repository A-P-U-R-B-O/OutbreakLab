"""
utils.py

Utility functions for OutbreakLab.
- Input validation for model parameters.
- Flexible parameter parsing and transformation.
- Potential hooks for future data operations (e.g., saving/loading, stats).

Author: OutbreakLab Team
"""

def validate_parameters(N: int, I0: int, R0: int, beta: float, gamma: float, days: int, dt: float = 1.0):
    """
    Validate SIR model parameters.
    Raises AssertionError if any parameter is out of range.
    """
    assert isinstance(N, int) and N > 0, "Total population N must be a positive integer."
    assert isinstance(I0, (int, float)) and 0 <= I0 <= N, "Initial infected I0 must be in 0..N."
    assert isinstance(R0, (int, float)) and 0 <= R0 <= N, "Initial recovered R0 must be in 0..N."
    assert (I0 + R0) <= N, "Sum of I0 and R0 must not exceed N."
    assert isinstance(beta, float) and 0 <= beta <= 1, "Beta (infection rate) must be in [0, 1]."
    assert isinstance(gamma, float) and 0 <= gamma <= 1, "Gamma (recovery rate) must be in [0, 1]."
    assert isinstance(days, int) and days > 0, "Days must be a positive integer."
    assert isinstance(dt, float) and dt > 0, "dt (timestep) must be positive."

def clamp(value, min_value, max_value):
    """
    Clamp a numeric value between min_value and max_value.
    """
    return max(min_value, min(value, max_value))

def to_int(value, default=0):
    """
    Convert value to int, with fallback to default.
    """
    try:
        return int(value)
    except Exception:
        return default

def to_float(value, default=0.0):
    """
    Convert value to float, with fallback to default.
    """
    try:
        return float(value)
    except Exception:
        return default
