import streamlit as st
import pandas as pd
import numpy as np
import io
import os
from pathlib import Path

# Fixed imports: remove 'src.' prefix for local modules in src/
from config import DEFAULTS, APP_TITLE, APP_DESCRIPTION, APP_ICON
from sir_model import (
    run_sir_simulation, 
    run_seir_simulation, 
    run_sirv_simulation, 
    run_seirv_simulation, 
    run_seird_simulation,    # <-- NEW
    get_epidemic_metrics
)
from visualization import (
    plot_sir, 
    plot_seir, 
    plot_sirv, 
    plot_seirv,
    plot_seird,             # <-- NEW
    plot_epidemic_metrics
)
from utils import validate_parameters, to_int, to_float

### --- Custom CSS Loading ---
def load_custom_css():
    css_path = Path(__file__).parent.parent / "assets" / "custom.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("Custom CSS file not found. Using default Streamlit styles.")

load_custom_css()

### --- Sidebar: App Info & Model Selection ---
st.set_page_config(page_title=APP_TITLE, page_icon="🦠", layout="wide")
st.sidebar.markdown(f"# {APP_ICON} {APP_TITLE}")
st.sidebar.info(APP_DESCRIPTION)

model_choice = st.sidebar.selectbox(
    "Choose epidemic model",
    ["SIR", "SEIR", "SIRV", "SEIRV", "SEIRD"],  # <-- Added SEIRD
    help="Select which compartmental model to simulate."
)

stochastic = st.sidebar.checkbox(
    "Stochastic simulation",
    value=False,
    help="Enable randomness in the simulation (Gillespie-like)."
)

if stochastic:
    seed = st.sidebar.number_input("Random seed", min_value=0, max_value=999999, value=42, help="Set to make results reproducible.")
else:
    seed = None

### --- Main Panel: Input Controls ---
st.markdown(f"## {APP_ICON} OutbreakLab: Interactive Epidemic Simulator")

with st.expander("ℹ️ How to use", expanded=True):
    st.markdown("""
    - **Set model parameters** or **upload your own CSV** (see example below).
    - Choose the **model type** and simulation options in the sidebar.
    - Click **Run Simulation** to view results, metrics, and plots.
    - Download data and figures for further analysis.
    """)
    # Add a download button for the example CSV
    example_csv_path = Path(__file__).parent.parent / "assets" / "example_data.csv"
    if example_csv_path.exists():
        with open(example_csv_path, "rb") as f:
            st.download_button(
                label="⬇️ Download example CSV",
                data=f,
                file_name="example_data.csv",
                mime="text/csv"
            )
    else:
        st.warning("Example CSV file not found.")

st.markdown("---")

### --- Input Mode: Manual vs. CSV Upload ---
input_mode = st.radio(
    "Input mode", 
    ["Manual Parameters", "Upload CSV"],
    horizontal=True
)

params = {}
uploaded_df = None

if input_mode == "Upload CSV":
    uploaded_file = st.file_uploader("Upload outbreak CSV", type=["csv"])
    initial_pop = {}
    df = None
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            # Get initial values from the first row
            initial_pop["susceptible"] = int(df["susceptible"].iloc[0]) if "susceptible" in df.columns else 0
            initial_pop["infected"] = int(df["infected"].iloc[0]) if "infected" in df.columns else 0
            initial_pop["recovered"] = int(df["recovered"].iloc[0]) if "recovered" in df.columns else 0
            if "exposed" in df.columns:
                initial_pop["exposed"] = int(df["exposed"].iloc[0])
            if "vaccinated" in df.columns:
                initial_pop["vaccinated"] = int(df["vaccinated"].iloc[0])
            if "deceased" in df.columns:
                initial_pop["deceased"] = int(df["deceased"].iloc[0])
            N = sum([v for k, v in initial_pop.items() if k != "deceased"])
            st.success("CSV imported successfully. Params auto-filled below.")
        except Exception as e:
            st.error(f"Failed to parse CSV: {e}")
            df = None
            N = DEFAULTS["N"]
            initial_pop = {}
    if uploaded_file and df is not None:
        # Show parameter input widgets with initial values from the CSV
        st.markdown("#### Initial Population")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            N = st.number_input("Total population (N)", min_value=1, max_value=100_000_000, value=N, step=100)
        with col2:
            I0 = st.number_input("Initially infected (I₀)", min_value=0, max_value=N, value=initial_pop.get("infected", 0))
        with col3:
            R0 = st.number_input("Initially recovered (R₀)", min_value=0, max_value=N, value=initial_pop.get("recovered", 0))
        with col4:
            if model_choice in ["SEIR", "SEIRV", "SEIRD"]:
                E0 = st.number_input("Initially exposed (E₀)", min_value=0, max_value=N, value=initial_pop.get("exposed", 0))
            else:
                E0 = 0
        with col5:
            if model_choice in ["SIRV", "SEIRV"]:
                V0 = st.number_input("Initially vaccinated (V₀)", min_value=0, max_value=N, value=initial_pop.get("vaccinated", 0))
            else:
                V0 = 0
        with col6:
            if model_choice == "SEIRD":
                D0 = st.number_input("Initially deceased (D₀)", min_value=0, max_value=100_000_000, value=initial_pop.get("deceased", 0))
            else:
                D0 = 0

        st.markdown("#### Model Parameters")
        col6, col7, col8, col9, col10, col11 = st.columns(6)
        with col6:
            beta = st.number_input("Infection rate (β)", min_value=0.0, max_value=2.0, value=DEFAULTS["beta"], step=0.01)
        with col7:
            if model_choice in ["SEIR", "SEIRV", "SEIRD"]:
                sigma = st.number_input("Incubation rate (σ)", min_value=0.0, max_value=2.0, value=DEFAULTS.get("sigma", 0.2), step=0.01)
            else:
                sigma = None
        with col8:
            gamma = st.number_input("Recovery rate (γ)", min_value=0.0, max_value=2.0, value=DEFAULTS["gamma"], step=0.01)
        with col9:
            if model_choice == "SEIRD":
                mu = st.number_input("Mortality rate (μ)", min_value=0.0, max_value=2.0, value=DEFAULTS.get("mu", 0.01), step=0.01)
            else:
                mu = None
        with col10:
            days = st.number_input("Simulation days", min_value=1, max_value=1000, value=len(df))
        with col11:
            if model_choice in ["SIRV", "SEIRV"]:
                vac_rate = st.number_input("Vaccination rate (ν)", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
            else:
                vac_rate = None

        params = dict(
            N=int(N), I0=int(I0), R0=int(R0), days=int(days),
            beta=float(beta), gamma=float(gamma), dt=DEFAULTS["dt"]
        )
        if model_choice in ["SEIR", "SEIRV", "SEIRD"]:
            params["E0"] = int(E0)
            params["sigma"] = float(sigma)
        if model_choice in ["SIRV", "SEIRV"]:
            params["V0"] = int(V0)
            params["nu"] = float(vac_rate)
        if model_choice == "SEIRD":
            params["D0"] = int(D0)
            params["mu"] = float(mu)
        uploaded_df = df
    else:
        params = {}
else:
    # Manual parameter input
    st.markdown("#### Initial Population")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        N = st.number_input("Total population (N)", min_value=1, max_value=100_000_000, value=DEFAULTS["N"], step=100)
    with col2:
        I0 = st.number_input("Initially infected (I₀)", min_value=0, max_value=N, value=DEFAULTS["I0"])
    with col3:
        R0 = st.number_input("Initially recovered (R₀)", min_value=0, max_value=N, value=DEFAULTS["R0"])
    with col4:
        if model_choice in ["SEIR", "SEIRV", "SEIRD"]:
            E0 = st.number_input("Initially exposed (E₀)", min_value=0, max_value=N, value=DEFAULTS.get("E0", 0))
        else:
            E0 = 0
    with col5:
        if model_choice in ["SIRV", "SEIRV"]:
            V0 = st.number_input("Initially vaccinated (V₀)", min_value=0, max_value=N, value=0)
        else:
            V0 = 0
    with col6:
        if model_choice == "SEIRD":
            D0 = st.number_input("Initially deceased (D₀)", min_value=0, max_value=100_000_000, value=DEFAULTS.get("D0", 0))
        else:
            D0 = 0

    st.markdown("#### Model Parameters")
    col6, col7, col8, col9, col10, col11 = st.columns(6)
    with col6:
        beta = st.number_input("Infection rate (β)", min_value=0.0, max_value=2.0, value=DEFAULTS["beta"], step=0.01)
    with col7:
        if model_choice in ["SEIR", "SEIRV", "SEIRD"]:
            sigma = st.number_input("Incubation rate (σ)", min_value=0.0, max_value=2.0, value=DEFAULTS.get("sigma", 0.2), step=0.01)
        else:
            sigma = None
    with col8:
        gamma = st.number_input("Recovery rate (γ)", min_value=0.0, max_value=2.0, value=DEFAULTS["gamma"], step=0.01)
    with col9:
        if model_choice == "SEIRD":
            mu = st.number_input("Mortality rate (μ)", min_value=0.0, max_value=2.0, value=DEFAULTS.get("mu", 0.01), step=0.01)
        else:
            mu = None
    with col10:
        days = st.number_input("Simulation days", min_value=1, max_value=1000, value=DEFAULTS["days"])
    with col11:
        if model_choice in ["SIRV", "SEIRV"]:
            vac_rate = st.number_input("Vaccination rate (ν)", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
        else:
            vac_rate = None

    params = dict(
        N=int(N), I0=int(I0), R0=int(R0), days=int(days),
        beta=float(beta), gamma=float(gamma), dt=DEFAULTS["dt"]
    )
    if model_choice in ["SEIR", "SEIRV", "SEIRD"]:
        params["E0"] = int(E0)
        params["sigma"] = float(sigma)
    if model_choice in ["SIRV", "SEIRV"]:
        params["V0"] = int(V0)
        params["nu"] = float(vac_rate)
    if model_choice == "SEIRD":
        params["D0"] = int(D0)
        params["mu"] = float(mu)

### --- Parameter Validation ---
if params:
    try:
        validate_parameters(
            N=params["N"], I0=params["I0"], R0=params["R0"],
            beta=params["beta"], gamma=params["gamma"],
            days=params["days"], dt=params["dt"]
        )
    except AssertionError as e:
        st.error(f"Parameter error: {e}")
        st.stop()

### --- Run Simulation ---
run_button = st.button("▶️ Run Simulation", type="primary", use_container_width=True)
if run_button and params:
    with st.spinner("Simulating outbreak..."):
        try:
            if model_choice == "SIR":
                S, I, R = run_sir_simulation(
                    S0=params["N"] - params["I0"] - params["R0"],
                    I0=params["I0"],
                    R0=params["R0"],
                    beta=params["beta"],
                    gamma=params["gamma"],
                    N=params["N"],
                    days=params["days"],
                    dt=params["dt"],
                    stochastic=stochastic,
                    seed=seed
                )
                metrics = get_epidemic_metrics(S, I, R)
                fig = plot_sir(S, I, R, params["days"])
                metrics_fig = plot_epidemic_metrics(metrics)
                result_df = pd.DataFrame({
                    "day": np.arange(len(S)),
                    "susceptible": S,
                    "infected": I,
                    "recovered": R
                })
            elif model_choice == "SEIR":
                res = run_seir_simulation(
                    S0=params["N"] - params["E0"] - params["I0"] - params["R0"],
                    E0=params["E0"],
                    I0=params["I0"],
                    R0=params["R0"],
                    beta=params["beta"],
                    sigma=params["sigma"],
                    gamma=params["gamma"],
                    N=params["N"],
                    days=params["days"],
                    dt=params["dt"],
                    stochastic=stochastic,
                    seed=seed
                )
                metrics = get_epidemic_metrics(res["S"], res["I"], res["R"])
                fig = plot_seir(res["S"], res["E"], res["I"], res["R"], params["days"])
                metrics_fig = plot_epidemic_metrics(metrics)
                result_df = pd.DataFrame({
                    "day": np.arange(len(res["S"])),
                    "susceptible": res["S"],
                    "exposed": res["E"],
                    "infected": res["I"],
                    "recovered": res["R"]
                })
            elif model_choice == "SIRV":
                res = run_sirv_simulation(
                    S0=params["N"] - params["I0"] - params["R0"] - params["V0"],
                    I0=params["I0"],
                    R0=params["R0"],
                    V0=params["V0"],
                    beta=params["beta"],
                    gamma=params["gamma"],
                    nu=params["nu"],
                    N=params["N"],
                    days=params["days"],
                    dt=params["dt"],
                    stochastic=stochastic,
                    seed=seed
                )
                metrics = get_epidemic_metrics(res["S"], res["I"], res["R"])
                fig = plot_sirv(res["S"], res["I"], res["R"], res["V"], params["days"])
                metrics_fig = plot_epidemic_metrics(metrics)
                result_df = pd.DataFrame({
                    "day": np.arange(len(res["S"])),
                    "susceptible": res["S"],
                    "infected": res["I"],
                    "recovered": res["R"],
                    "vaccinated": res["V"]
                })
            elif model_choice == "SEIRV":
                res = run_seirv_simulation(
                    S0=params["N"] - params["E0"] - params["I0"] - params["R0"] - params["V0"],
                    E0=params["E0"],
                    I0=params["I0"],
                    R0=params["R0"],
                    V0=params["V0"],
                    beta=params["beta"],
                    sigma=params["sigma"],
                    gamma=params["gamma"],
                    nu=params["nu"],
                    N=params["N"],
                    days=params["days"],
                    dt=params["dt"],
                    stochastic=stochastic,
                    seed=seed
                )
                metrics = get_epidemic_metrics(res["S"], res["I"], res["R"])
                fig = plot_seirv(res["S"], res["E"], res["I"], res["R"], res["V"], params["days"])
                metrics_fig = plot_epidemic_metrics(metrics)
                result_df = pd.DataFrame({
                    "day": np.arange(len(res["S"])),
                    "susceptible": res["S"],
                    "exposed": res["E"],
                    "infected": res["I"],
                    "recovered": res["R"],
                    "vaccinated": res["V"]
                })
            elif model_choice == "SEIRD":
                res = run_seird_simulation(
                    S0=params["N"] - params["E0"] - params["I0"] - params["R0"],
                    E0=params["E0"],
                    I0=params["I0"],
                    R0=params["R0"],
                    D0=params["D0"],
                    beta=params["beta"],
                    sigma=params["sigma"],
                    gamma=params["gamma"],
                    mu=params["mu"],
                    N=params["N"],
                    days=params["days"],
                    dt=params["dt"],
                    stochastic=stochastic,
                    seed=seed
                )
                # Note: For SEIRD, you may want a custom metrics function for D as well
                metrics = get_epidemic_metrics(res["S"], res["I"], res["R"])
                fig = plot_seird(res["S"], res["E"], res["I"], res["R"], res["D"], params["days"])
                metrics_fig = plot_epidemic_metrics(metrics)
                result_df = pd.DataFrame({
                    "day": np.arange(len(res["S"])),
                    "susceptible": res["S"],
                    "exposed": res["E"],
                    "infected": res["I"],
                    "recovered": res["R"],
                    "deceased": res["D"]
                })
            else:
                st.error("Unknown model selected.")
                st.stop()
        except Exception as e:
            st.error(f"Simulation failed: {e}")
            st.stop()

    st.success("Simulation complete! See results below.")

    ### --- Results Display ---
    col1, col2 = st.columns([2,1])
    with col1:
        st.pyplot(fig, use_container_width=True)
    with col2:
        st.markdown("#### Key Epidemic Metrics")
        for k, v in metrics.items():
            st.metric(label=k.replace("_", " ").capitalize(), value=round(v, 2))
        st.pyplot(metrics_fig, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Data Table")
    st.dataframe(result_df, use_container_width=True, hide_index=True)

    ### --- Download Buttons (Data & Plots) ---
    col3, col4, col5 = st.columns(3)
    with col3:
        csv_buf = io.StringIO()
        result_df.to_csv(csv_buf, index=False)
        st.download_button(
            label="⬇️ Download Data (CSV)",
            data=csv_buf.getvalue(),
            file_name="outbreak_results.csv",
            mime="text/csv"
        )
    with col4:
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format="png", bbox_inches="tight")
        st.download_button(
            label="⬇️ Download Plot (PNG)",
            data=img_buf.getvalue(),
            file_name="outbreak_plot.png",
            mime="image/png"
        )
    with col5:
        img2_buf = io.BytesIO()
        metrics_fig.savefig(img2_buf, format="png", bbox_inches="tight")
        st.download_button(
            label="⬇️ Download Metrics (PNG)",
            data=img2_buf.getvalue(),
            file_name="metrics_plot.png",
            mime="image/png"
        )

    st.markdown("---")
    st.markdown("##### Try a different scenario or upload another file to continue exploring!")

### --- Footer ---
st.markdown(
    """
    <hr>
    <div style='text-align:center; color:#888; font-size:0.9em;'>
    OutbreakLab &copy; 2025 | <a href='https://github.com/A-P-U-R-B-O/OutbreakLab' target='_blank'>GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
            )
