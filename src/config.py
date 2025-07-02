"""
config.py

Default configuration and constants for OutbreakLab.
Modify these values to change the default simulation parameters or app-wide settings.

Author: OutbreakLab Team
"""

DEFAULTS = {
    "N": 1000,         # Default total population
    "I0": 1,           # Default initial infected
    "R0": 0,           # Default initial recovered
    "beta": 0.3,       # Default infection rate
    "gamma": 0.1,      # Default recovery rate
    "days": 100,       # Default simulation days
    "dt": 1.0,         # Default timestep (days)
    # SEIR-specific defaults (for extensibility)
    "E0": 0,           # Default initial exposed (SEIR)
    "sigma": 0.2       # Default rate of progression from exposed to infected (SEIR)
}

APP_TITLE = "OutbreakLab"
APP_DESCRIPTION = (
    "OutbreakLab is an interactive web app for simulating and visualizing "
    "infectious disease outbreaks using compartmental models such as SIR and SEIR."
)
APP_ICON = ":microbe:"
