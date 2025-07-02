"""
OutbreakLab

A modular package for infectious disease simulation and visualization.
This package currently supports the classic SIR (Susceptible-Infected-Recovered) model, 
with extensible structure for future epidemiological models (SEIR, SIRS, etc.).

Organized modules:
- sir_model: Core SIR simulation logic
- visualization: Plotting and visualization helpers
- utils: Validation and general utilities
- config: Default constants and configuration

Usage Example:
--------------
from src.sir_model import run_sir_simulation
from src.visualization import plot_sir

# Run simulation
S, I, R = run_sir_simulation(S0=999, I0=1, R0=0, beta=0.3, gamma=0.1, N=1000, days=100)

# Plot results
fig = plot_sir(S, I, R, days=100)
"""

from .sir_model import run_sir_simulation
from .visualization import plot_sir
from .utils import validate_parameters
from .config import DEFAULTS

__all__ = [
    "run_sir_simulation",
    "plot_sir",
    "validate_parameters",
    "DEFAULTS"
]
