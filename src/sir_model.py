"""
sir_model.py

Advanced SIR and compartmental epidemic model simulation logic for OutbreakLab.
Includes:
    - Classic SIR solver (Euler method)
    - Optional stochastic (random) SIR simulation
    - Optional stochastic SEIR simulation
    - Support for additional compartments (e.g., SEIR, SIRS) via extension
    - Parameter validation and result packaging

Author: OutbreakLab Team
"""

import numpy as np
from typing import Tuple, Dict, List, Optional

def run_sir_simulation(
    S0: int, I0: int, R0: int, 
    beta: float, gamma: float, 
    N: int, days: int,
    dt: float = 1.0,
    stochastic: bool = False,
    seed: Optional[int] = None
) -> Tuple[List[float], List[float], List[float]]:
    """
    Simulate the SIR model over a number of days.

    Parameters:
        S0, I0, R0: Initial susceptible, infected, recovered counts
        beta: Infection rate per contact per day
        gamma: Recovery rate per day
        N: Total population
        days: Number of days to simulate
        dt: Timestep (days)
        stochastic: Whether to use a stochastic simulation (Gillespie-like)
        seed: Optional random seed for reproducibility

    Returns:
        S, I, R: Lists of susceptible, infected, recovered over time
    """
    steps = int(days / dt)
    S, I, R = [S0], [I0], [R0]
    if stochastic and seed is not None:
        np.random.seed(seed)

    for step in range(steps):
        s, i, r = S[-1], I[-1], R[-1]
        if stochastic:
            # Stochastic transitions (binomial sampling)
            new_infected = np.random.binomial(int(s), 1 - np.exp(-beta * i / N * dt))
            new_recovered = np.random.binomial(int(i), 1 - np.exp(-gamma * dt))
        else:
            new_infected = beta * s * i / N * dt
            new_recovered = gamma * i * dt

        s_new = max(s - new_infected, 0)
        i_new = max(i + new_infected - new_recovered, 0)
        r_new = min(r + new_recovered, N)

        # Ensure population is conserved (numerical safety)
        if s_new + i_new + r_new > N:
            excess = s_new + i_new + r_new - N
            r_new -= excess # remove from R (safe for SIR)

        S.append(s_new)
        I.append(i_new)
        R.append(r_new)
        if i_new < 1e-6:
            # Epidemic ended, fill remaining with steady state
            S += [s_new]*(steps-step-1)
            I += [0]*(steps-step-1)
            R += [r_new]*(steps-step-1)
            break
    return S, I, R

def run_seir_simulation(
    S0: int, E0: int, I0: int, R0: int,
    beta: float, sigma: float, gamma: float,
    N: int, days: int, dt: float = 1.0,
    stochastic: bool = False,
    seed: Optional[int] = None
) -> Dict[str, List[float]]:
    """
    Run an SEIR (Susceptible-Exposed-Infected-Recovered) model.
    Parameters:
        S0, E0, I0, R0: initial values for compartments
        beta: Transmission rate
        sigma: Rate of progression from exposed to infected (1/incubation period)
        gamma: Recovery rate
        N: Population
        days: Number of days to simulate
        dt: Timestep (days)
        stochastic: Whether to use a stochastic simulation (Gillespie-like)
        seed: Optional random seed for reproducibility
    Returns:
        Dict with lists for S, E, I, R
    """
    steps = int(days / dt)
    S, E, I, R = [S0], [E0], [I0], [R0]
    if stochastic and seed is not None:
        np.random.seed(seed)
    for step in range(steps):
        s, e, i, r = S[-1], E[-1], I[-1], R[-1]
        if stochastic:
            # Stochastic transitions (binomial sampling)
            p_SE = 1 - np.exp(-beta * i / N * dt) if N > 0 else 0
            p_EI = 1 - np.exp(-sigma * dt)
            p_IR = 1 - np.exp(-gamma * dt)
            new_exposed = np.random.binomial(int(s), p_SE)
            new_infected = np.random.binomial(int(e), p_EI)
            new_recovered = np.random.binomial(int(i), p_IR)
        else:
            new_exposed = beta * s * i / N * dt
            new_infected = sigma * e * dt
            new_recovered = gamma * i * dt

        s_new = max(s - new_exposed, 0)
        e_new = max(e + new_exposed - new_infected, 0)
        i_new = max(i + new_infected - new_recovered, 0)
        r_new = min(r + new_recovered, N)

        # Ensure population conservation
        if s_new + e_new + i_new + r_new > N:
            excess = s_new + e_new + i_new + r_new - N
            r_new -= excess

        S.append(s_new)
        E.append(e_new)
        I.append(i_new)
        R.append(r_new)
        if i_new < 1e-6 and e_new < 1e-6:
            # Disease died out
            S += [s_new]*(steps-step-1)
            E += [e_new]*(steps-step-1)
            I += [0]*(steps-step-1)
            R += [r_new]*(steps-step-1)
            break
    return {'S': S, 'E': E, 'I': I, 'R': R}

def get_epidemic_metrics(S: List[float], I: List[float], R: List[float], dt: float = 1.0) -> Dict[str, float]:
    """
    Compute summary statistics for an SIR epidemic curve.
    Returns:
        - peak_infected: Maximum number of infected
        - peak_day: Day at which peak occurs
        - total_infected: Final size of epidemic (R[-1])
        - duration: Duration until cases < 1
    """
    peak_infected = max(I)
    peak_day = I.index(peak_infected) * dt
    total_infected = R[-1]
    duration = next((i*dt for i, v in enumerate(I) if v < 1), len(I)*dt)
    return dict(
        peak_infected=peak_infected,
        peak_day=peak_day,
        total_infected=total_infected,
        duration=duration
        )
