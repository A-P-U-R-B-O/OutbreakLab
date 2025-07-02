"""
Unit tests for src.sir_model (SIR and SEIR simulation functions) in OutbreakLab.
Covers:
- Deterministic SIR simulation
- Stochastic SIR simulation (with reproducible seed)
- SEIR simulation
- Epidemic metrics computation

Author: OutbreakLab Team
"""

import pytest
from src.sir_model import run_sir_simulation, run_seir_simulation, get_epidemic_metrics

def test_run_sir_simulation_deterministic():
    S, I, R = run_sir_simulation(S0=999, I0=1, R0=0, beta=0.3, gamma=0.1, N=1000, days=50)
    assert len(S) == 51
    assert len(I) == 51
    assert len(R) == 51
    # Population is (almost) conserved
    for s, i, r in zip(S, I, R):
        assert abs(s + i + r - 1000) < 1e-3
    # Epidemic should eventually decline
    assert I[-1] < 1

def test_run_sir_simulation_stochastic_reproducible():
    S1, I1, R1 = run_sir_simulation(S0=100, I0=1, R0=0, beta=0.3, gamma=0.1, N=101, days=20, stochastic=True, seed=42)
    S2, I2, R2 = run_sir_simulation(S0=100, I0=1, R0=0, beta=0.3, gamma=0.1, N=101, days=20, stochastic=True, seed=42)
    assert S1 == pytest.approx(S2)
    assert I1 == pytest.approx(I2)
    assert R1 == pytest.approx(R2)

def test_run_seir_simulation():
    res = run_seir_simulation(S0=999, E0=0, I0=1, R0=0, beta=0.3, sigma=0.2, gamma=0.1, N=1000, days=60)
    S, E, I, R = res["S"], res["E"], res["I"], res["R"]
    assert len(S) == 61
    assert len(E) == 61
    assert len(I) == 61
    assert len(R) == 61
    # Population is (almost) conserved
    for s, e, i, r in zip(S, E, I, R):
        assert abs(s + e + i + r - 1000) < 1e-3
    # Epidemic should eventually decline
    assert I[-1] < 1 and E[-1] < 1

def test_get_epidemic_metrics():
    S, I, R = run_sir_simulation(S0=999, I0=1, R0=0, beta=0.3, gamma=0.1, N=1000, days=50)
    metrics = get_epidemic_metrics(S, I, R)
    assert "peak_infected" in metrics
    assert "peak_day" in metrics
    assert "total_infected" in metrics
    assert "duration" in metrics
    assert metrics["peak_infected"] > 0
    assert metrics["peak_day"] >= 0
    assert metrics["total_infected"] <= 1000
    assert metrics["duration"] > 0
