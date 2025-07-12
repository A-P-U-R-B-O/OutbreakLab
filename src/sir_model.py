"""
sir_model.py

Advanced SIR and compartmental epidemic model simulation logic for OutbreakLab.
Includes:
    - Classic SIR solver (Euler method)
    - Optional stochastic (random) SIR simulation
    - Optional stochastic SEIR simulation
    - Advanced SIRV (Susceptible-Infected-Recovered-Vaccinated) model (deterministic and stochastic)
    - SEIRV (Susceptible-Exposed-Infected-Recovered-Vaccinated) model (deterministic and stochastic)
    - SEIRD (Susceptible-Exposed-Infected-Recovered-Deceased) model (deterministic and stochastic)
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
            r_new -= excess

        S.append(s_new)
        I.append(i_new)
        R.append(r_new)
        if i_new < 1e-6:
            # Epidemic ended, fill remaining with steady state
            S += [s_new] * (steps - step - 1)
            I += [0] * (steps - step - 1)
            R += [r_new] * (steps - step - 1)
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
            S += [s_new] * (steps - step - 1)
            E += [e_new] * (steps - step - 1)
            I += [0] * (steps - step - 1)
            R += [r_new] * (steps - step - 1)
            break
    return {'S': S, 'E': E, 'I': I, 'R': R}

def run_sirv_simulation(
    S0: int, I0: int, R0: int, V0: int,
    beta: float, gamma: float, nu: float,
    N: int, days: int, dt: float = 1.0,
    stochastic: bool = False,
    seed: Optional[int] = None
) -> Dict[str, List[float]]:
    """
    Run a SIRV (Susceptible-Infected-Recovered-Vaccinated) model simulation.
    Returns:
        Dict with lists for S, I, R, V
    """
    steps = int(days / dt)
    S, I, R, V = [S0], [I0], [R0], [V0]
    if stochastic and seed is not None:
        np.random.seed(seed)
    for step in range(steps):
        s, i, r, v = S[-1], I[-1], R[-1], V[-1]
        if stochastic:
            p_inf = 1 - np.exp(-beta * i / N * dt) if N > 0 else 0
            p_vac = 1 - np.exp(-nu * dt)
            p_rec = 1 - np.exp(-gamma * dt)
            new_infected = np.random.binomial(int(s), p_inf)
            new_vaccinated = np.random.binomial(int(s - new_infected), p_vac) if (s - new_infected) > 0 else 0
            new_recovered = np.random.binomial(int(i), p_rec)
        else:
            new_infected = beta * s * i / N * dt
            new_vaccinated = nu * s * dt
            new_recovered = gamma * i * dt

        s_new = max(s - new_infected - new_vaccinated, 0)
        i_new = max(i + new_infected - new_recovered, 0)
        r_new = min(r + new_recovered, N)
        v_new = min(v + new_vaccinated, N)

        if s_new + i_new + r_new + v_new > N:
            excess = s_new + i_new + r_new + v_new - N
            v_new -= excess

        S.append(s_new)
        I.append(i_new)
        R.append(r_new)
        V.append(v_new)
        if i_new < 1e-6:
            S += [s_new] * (steps - step - 1)
            I += [0] * (steps - step - 1)
            R += [r_new] * (steps - step - 1)
            V += [v_new] * (steps - step - 1)
            break
    return {'S': S, 'I': I, 'R': R, 'V': V}

def run_seirv_simulation(
    S0: int, E0: int, I0: int, R0: int, V0: int,
    beta: float, sigma: float, gamma: float, nu: float,
    N: int, days: int, dt: float = 1.0,
    stochastic: bool = False,
    seed: Optional[int] = None
) -> Dict[str, List[float]]:
    """
    Run an SEIRV (Susceptible-Exposed-Infected-Recovered-Vaccinated) model simulation.
    Returns:
        Dict with lists for S, E, I, R, V
    """
    steps = int(days / dt)
    S, E, I, R, V = [S0], [E0], [I0], [R0], [V0]
    if stochastic and seed is not None:
        np.random.seed(seed)
    for step in range(steps):
        s, e, i, r, v = S[-1], E[-1], I[-1], R[-1], V[-1]
        if stochastic:
            p_inf = 1 - np.exp(-beta * i / N * dt) if N > 0 else 0
            p_vac = 1 - np.exp(-nu * dt)
            p_ei = 1 - np.exp(-sigma * dt)
            p_ir = 1 - np.exp(-gamma * dt)
            new_exposed = np.random.binomial(int(s), p_inf)
            new_vaccinated = np.random.binomial(int(s - new_exposed), p_vac) if (s - new_exposed) > 0 else 0
            new_infected = np.random.binomial(int(e), p_ei)
            new_recovered = np.random.binomial(int(i), p_ir)
        else:
            new_exposed = beta * s * i / N * dt
            new_vaccinated = nu * s * dt
            new_infected = sigma * e * dt
            new_recovered = gamma * i * dt

        s_new = max(s - new_exposed - new_vaccinated, 0)
        e_new = max(e + new_exposed - new_infected, 0)
        i_new = max(i + new_infected - new_recovered, 0)
        r_new = min(r + new_recovered, N)
        v_new = min(v + new_vaccinated, N)

        if s_new + e_new + i_new + r_new + v_new > N:
            excess = s_new + e_new + i_new + r_new + v_new - N
            v_new -= excess

        S.append(s_new)
        E.append(e_new)
        I.append(i_new)
        R.append(r_new)
        V.append(v_new)
        if i_new < 1e-6 and e_new < 1e-6:
            S += [s_new] * (steps - step - 1)
            E += [e_new] * (steps - step - 1)
            I += [0] * (steps - step - 1)
            R += [r_new] * (steps - step - 1)
            V += [v_new] * (steps - step - 1)
            break
    return {'S': S, 'E': E, 'I': I, 'R': R, 'V': V}

def run_seird_simulation(
    S0: int, E0: int, I0: int, R0: int, D0: int,
    beta: float, sigma: float, gamma: float, mu: float,
    N: int, days: int, dt: float = 1.0,
    stochastic: bool = False,
    seed: Optional[int] = None
) -> Dict[str, List[float]]:
    """
    Run an SEIRD (Susceptible-Exposed-Infected-Recovered-Deceased) model simulation.

    Compartments:
        S: Susceptible
        E: Exposed
        I: Infected
        R: Recovered
        D: Deceased

    Parameters:
        beta: Infection rate
        sigma: Incubation rate (E->I)
        gamma: Recovery rate (I->R)
        mu: Disease-induced mortality rate (I->D)
        N: Total population (excluding deceased)
        days: Simulation days
        dt: Time step
        stochastic: If True, uses stochastic simulation
        seed: Random seed

    Returns:
        Dict with lists for S, E, I, R, D
    """
    steps = int(days / dt)
    S, E, I, R, D = [S0], [E0], [I0], [R0], [D0]
    if stochastic and seed is not None:
        np.random.seed(seed)
    for step in range(steps):
        s, e, i, r, d = S[-1], E[-1], I[-1], R[-1], D[-1]
        if stochastic:
            p_SE = 1 - np.exp(-beta * i / N * dt) if N > 0 else 0
            p_EI = 1 - np.exp(-sigma * dt)
            p_IR = 1 - np.exp(-gamma * dt)
            p_ID = 1 - np.exp(-mu * dt)
            new_exposed = np.random.binomial(int(s), p_SE)
            new_infected = np.random.binomial(int(e), p_EI)
            # Partition infected into recovered or deceased
            new_recovered = np.random.binomial(int(i), p_IR)
            new_deceased = np.random.binomial(int(i - new_recovered), p_ID) if (i - new_recovered) > 0 else 0
        else:
            new_exposed = beta * s * i / N * dt
            new_infected = sigma * e * dt
            total_out = gamma * i * dt + mu * i * dt
            if total_out > i:
                # Prevent negative I due to large dt
                gamma_adj = (gamma * i * dt) / total_out if total_out > 0 else 0
                mu_adj = (mu * i * dt) / total_out if total_out > 0 else 0
                new_recovered = gamma_adj * i
                new_deceased = mu_adj * i
            else:
                new_recovered = gamma * i * dt
                new_deceased = mu * i * dt

        s_new = max(s - new_exposed, 0)
        e_new = max(e + new_exposed - new_infected, 0)
        i_new = max(i + new_infected - new_recovered - new_deceased, 0)
        r_new = min(r + new_recovered, N)
        d_new = d + new_deceased  # Deaths accumulate

        # Ensure population conservation (S+E+I+R <= N, D accumulates separately)
        if s_new + e_new + i_new + r_new > N:
            excess = s_new + e_new + i_new + r_new - N
            r_new -= excess

        S.append(s_new)
        E.append(e_new)
        I.append(i_new)
        R.append(r_new)
        D.append(d_new)
        if i_new < 1e-6 and e_new < 1e-6:
            S += [s_new] * (steps - step - 1)
            E += [e_new] * (steps - step - 1)
            I += [0] * (steps - step - 1)
            R += [r_new] * (steps - step - 1)
            D += [d_new] * (steps - step - 1)
            break
    return {'S': S, 'E': E, 'I': I, 'R': R, 'D': D}

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
    duration = next((i * dt for i, v in enumerate(I) if v < 1), len(I) * dt)
    return dict(
        peak_infected=peak_infected,
        peak_day=peak_day,
        total_infected=total_infected,
        duration=duration
            )
