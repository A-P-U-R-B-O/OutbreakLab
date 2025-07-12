"""
visualization.py

Visualization helpers for OutbreakLab.
- Flexible plotting for SIR, SEIR, SIRV, SEIRV, SEIRD, and similar compartmental models
- Customizable appearance (colors, labels, titles)
- Ready for Streamlit and Jupyter integration

Author: OutbreakLab Team
"""

import matplotlib.pyplot as plt
from typing import List, Dict, Optional

def plot_sir(
    S: List[float], 
    I: List[float], 
    R: List[float], 
    days: int, 
    dt: float = 1.0, 
    title: str = "SIR Model Simulation",
    show_legend: bool = True,
    custom_colors: Optional[Dict[str, str]] = None
):
    """
    Plot SIR model results.
    """
    t = [i * dt for i in range(len(S))]
    colors = custom_colors or {"S": "#1f77b4", "I": "#d62728", "R": "#2ca02c"}

    fig, ax = plt.subplots()
    ax.plot(t, S, label="Susceptible", color=colors["S"], linewidth=2)
    ax.plot(t, I, label="Infected", color=colors["I"], linewidth=2)
    ax.plot(t, R, label="Recovered", color=colors["R"], linewidth=2)
    ax.set_xlabel("Days")
    ax.set_ylabel("Number of Individuals")
    ax.set_title(title)
    if show_legend:
        ax.legend()
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
    fig.tight_layout()
    return fig

def plot_seir(
    S: List[float],
    E: List[float],
    I: List[float],
    R: List[float],
    days: int,
    dt: float = 1.0,
    title: str = "SEIR Model Simulation",
    show_legend: bool = True,
    custom_colors: Optional[Dict[str, str]] = None
):
    """
    Plot SEIR model results.
    """
    t = [i * dt for i in range(len(S))]
    colors = custom_colors or {"S": "#1f77b4", "E": "#ff7f0e", "I": "#d62728", "R": "#2ca02c"}

    fig, ax = plt.subplots()
    ax.plot(t, S, label="Susceptible", color=colors["S"], linewidth=2)
    ax.plot(t, E, label="Exposed", color=colors["E"], linewidth=2)
    ax.plot(t, I, label="Infected", color=colors["I"], linewidth=2)
    ax.plot(t, R, label="Recovered", color=colors["R"], linewidth=2)
    ax.set_xlabel("Days")
    ax.set_ylabel("Number of Individuals")
    ax.set_title(title)
    if show_legend:
        ax.legend()
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
    fig.tight_layout()
    return fig

def plot_sirv(
    S: List[float],
    I: List[float],
    R: List[float],
    V: List[float],
    days: int,
    dt: float = 1.0,
    title: str = "SIRV Model Simulation",
    show_legend: bool = True,
    custom_colors: Optional[Dict[str, str]] = None
):
    """
    Plot SIRV model results.
    """
    t = [i * dt for i in range(len(S))]
    colors = custom_colors or {
        "S": "#1f77b4",   # blue
        "I": "#d62728",   # red
        "R": "#2ca02c",   # green
        "V": "#9467bd"    # purple
    }

    fig, ax = plt.subplots()
    ax.plot(t, S, label="Susceptible", color=colors["S"], linewidth=2)
    ax.plot(t, I, label="Infected", color=colors["I"], linewidth=2)
    ax.plot(t, R, label="Recovered", color=colors["R"], linewidth=2)
    ax.plot(t, V, label="Vaccinated", color=colors["V"], linewidth=2)
    ax.set_xlabel("Days")
    ax.set_ylabel("Number of Individuals")
    ax.set_title(title)
    if show_legend:
        ax.legend()
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
    fig.tight_layout()
    return fig

def plot_seirv(
    S: List[float],
    E: List[float],
    I: List[float],
    R: List[float],
    V: List[float],
    days: int,
    dt: float = 1.0,
    title: str = "SEIRV Model Simulation",
    show_legend: bool = True,
    custom_colors: Optional[Dict[str, str]] = None
):
    """
    Plot SEIRV model results.

    Parameters:
        S, E, I, R, V: Lists of counts for each compartment
        days: Number of days simulated
        dt: Time step size
        title: Plot title
        show_legend: Whether to display legend
        custom_colors: Dict for line colors
    Returns:
        Matplotlib Figure object
    """
    t = [i * dt for i in range(len(S))]
    colors = custom_colors or {
        "S": "#1f77b4",   # blue
        "E": "#ff7f0e",   # orange
        "I": "#d62728",   # red
        "R": "#2ca02c",   # green
        "V": "#9467bd"    # purple
    }

    fig, ax = plt.subplots()
    ax.plot(t, S, label="Susceptible", color=colors["S"], linewidth=2)
    ax.plot(t, E, label="Exposed", color=colors["E"], linewidth=2)
    ax.plot(t, I, label="Infected", color=colors["I"], linewidth=2)
    ax.plot(t, R, label="Recovered", color=colors["R"], linewidth=2)
    ax.plot(t, V, label="Vaccinated", color=colors["V"], linewidth=2)
    ax.set_xlabel("Days")
    ax.set_ylabel("Number of Individuals")
    ax.set_title(title)
    if show_legend:
        ax.legend()
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
    fig.tight_layout()
    return fig

def plot_seird(
    S: List[float],
    E: List[float],
    I: List[float],
    R: List[float],
    D: List[float],
    days: int,
    dt: float = 1.0,
    title: str = "SEIRD Model Simulation",
    show_legend: bool = True,
    custom_colors: Optional[Dict[str, str]] = None
):
    """
    Plot SEIRD model results.

    Parameters:
        S, E, I, R, D: Lists of counts for each compartment
        days: Number of days simulated
        dt: Time step size
        title: Plot title
        show_legend: Whether to display legend
        custom_colors: Dict for line colors
    Returns:
        Matplotlib Figure object
    """
    t = [i * dt for i in range(len(S))]
    colors = custom_colors or {
        "S": "#1f77b4",   # blue
        "E": "#ff7f0e",   # orange
        "I": "#d62728",   # red
        "R": "#2ca02c",   # green
        "D": "#393b79"    # dark blue
    }

    fig, ax = plt.subplots()
    ax.plot(t, S, label="Susceptible", color=colors["S"], linewidth=2)
    ax.plot(t, E, label="Exposed", color=colors["E"], linewidth=2)
    ax.plot(t, I, label="Infected", color=colors["I"], linewidth=2)
    ax.plot(t, R, label="Recovered", color=colors["R"], linewidth=2)
    ax.plot(t, D, label="Deceased", color=colors["D"], linewidth=2)
    ax.set_xlabel("Days")
    ax.set_ylabel("Number of Individuals")
    ax.set_title(title)
    if show_legend:
        ax.legend()
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
    fig.tight_layout()
    return fig

def plot_epidemic_metrics(metrics: Dict[str, float], title: str = "Epidemic Metrics Summary"):
    """
    Display a summary bar plot of key epidemic metrics.
    """
    keys = list(metrics.keys())
    values = [metrics[k] for k in keys]
    fig, ax = plt.subplots()
    ax.bar(keys, values, color="#7f7f7f")
    ax.set_ylabel("Value")
    ax.set_title(title)
    for i, v in enumerate(values):
        ax.text(i, v, f"{v:.1f}", ha='center', va='bottom')
    fig.tight_layout()
    return fig

def plot_generic_compartments(
    results: Dict[str, List[float]],
    days: int,
    dt: float = 1.0,
    title: str = "Compartment Model Simulation",
    show_legend: bool = True,
    custom_colors: Optional[Dict[str, str]] = None,
    compartment_labels: Optional[Dict[str, str]] = None
):
    """
    General-purpose plotter for arbitrary compartment model results.
    Use for any new or extended model.
    """
    t = [i * dt for i in range(len(next(iter(results.values()))))]
    default_colors = {
        "S": "#1f77b4",   # blue
        "E": "#ff7f0e",   # orange
        "I": "#d62728",   # red
        "R": "#2ca02c",   # green
        "V": "#9467bd",   # purple
        "D": "#393b79",   # dark blue for Deceased
    }
    colors = custom_colors or default_colors
    labels = compartment_labels or {
        "S": "Susceptible",
        "E": "Exposed",
        "I": "Infected",
        "R": "Recovered",
        "V": "Vaccinated",
        "D": "Deceased"
    }

    fig, ax = plt.subplots()
    for comp, vals in results.items():
        ax.plot(t, vals, label=labels.get(comp, comp), color=colors.get(comp, None), linewidth=2)
    ax.set_xlabel("Days")
    ax.set_ylabel("Number of Individuals")
    ax.set_title(title)
    if show_legend:
        ax.legend()
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
    fig.tight_layout()
    return fig
