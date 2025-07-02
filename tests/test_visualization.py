"""
Unit tests for src.visualization in OutbreakLab.
Covers:
- SIR model plotting
- SEIR model plotting
- Epidemic metrics summary plotting

Author: OutbreakLab Team
"""

import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend for testing
import matplotlib.pyplot as plt

from src.visualization import plot_sir, plot_seir, plot_epidemic_metrics

def test_plot_sir_generates_figure():
    S = [1000, 900, 800, 700]
    I = [0, 50, 100, 50]
    R = [0, 50, 100, 250]
    days = 3
    fig = plot_sir(S, I, R, days)
    assert isinstance(fig, plt.Figure)
    # Optionally, check for axes labels, legend, or title
    ax = fig.axes[0]
    assert ax.get_xlabel().lower() == "days"
    assert ax.get_ylabel().lower() in ("number of individuals", "population")
    assert ax.get_title() != ""

def test_plot_seir_generates_figure():
    S = [1000, 900, 800, 700]
    E = [0, 20, 40, 20]
    I = [0, 30, 60, 30]
    R = [0, 50, 100, 250]
    days = 3
    fig = plot_seir(S, E, I, R, days)
    assert isinstance(fig, plt.Figure)
    ax = fig.axes[0]
    assert ax.get_xlabel().lower() == "days"
    assert ax.get_ylabel().lower() in ("number of individuals", "population")
    assert ax.get_title() != ""

def test_plot_epidemic_metrics_generates_figure():
    metrics = {
        "peak_infected": 250,
        "peak_day": 20,
        "total_infected": 800,
        "duration": 45
    }
    fig = plot_epidemic_metrics(metrics)
    assert isinstance(fig, plt.Figure)
    ax = fig.axes[0]
    assert ax.get_title() != ""
    # Optionally, check that all metrics are present in x-ticks
    xtick_labels = [tick.get_text() for tick in ax.get_xticklabels()]
    for key in metrics.keys():
        assert key in xtick_labels or key.replace('_', ' ') in xtick_labels
