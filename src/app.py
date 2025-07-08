import streamlit as st
import pandas as pd
import numpy as np
import io
import os
from pathlib import Path

# Fixed imports: remove 'src.' prefix for local modules in src/
from config import DEFAULTS, APP_TITLE, APP_DESCRIPTION, APP_ICON
from sir_model import run_sir_simulation, run_seir_simulation, get_epidemic_metrics
from visualization import plot_sir, plot_seir, plot_epidemic_metrics
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
    ["SIR", "SEIR"],
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

def parse_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        required_cols = {"susceptible", "infected", "recovered"}
        if model_choice == "SEIR":
            required_cols.add("exposed")
        if not required_cols.issubset(set(df.columns)):
            st.error(f"CSV must contain columns: {', '.join(required_cols)}")
            return None, None
        N = int(df.iloc[0][list(required_cols)].sum())
        days = len(df) - 1
        # Prepare params for simulation
        params = {
            "N": N,
            "S0": int(df["susceptible"][0]),
            "I0": int(df["infected"][0]),
            "R0": int(df["recovered"][0]),
            "days": days,
            "dt": 1.0
        }
        if model_choice == "SEIR":
            params["E0"] = int(df["exposed"][0])
        return params, df
    except Exception as e:
        st.error(f"Failed to parse CSV: {e}")
        return None, None

uploaded_df = None
if input_mode == "Upload CSV":
    uploaded_file = st.file_uploader("Upload outbreak CSV", type=["csv"])
    if uploaded_file:
        params, uploaded_df = parse_csv(uploaded_file)
        if params:
            st.success("CSV imported successfully. Params auto-filled below.")
else:
    # Manual parameter input
    st.markdown("#### Initial Population")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        N = st.number_input("Total population (N)", min_value=1, max_value=100_000_000, value=DEFAULTS["N"], step=100)
    with col2:
        I0 = st.number_input("Initially infected (I₀)", min_value=0, max_value=N, value=DEFAULTS["I0"])
    with col3:
        R0 = st.number_input("Initially recovered (R₀)", min_value=0, max_value=N, value=DEFAULTS["R0"])
    if model_choice == "SEIR":
        with col4:
            E0 = st.number_input("Initially exposed (E₀)", min_value=0, max_value=N, value=DEFAULTS.get("E0", 0))
    else:
        E0 = 0

    st.markdown("#### Model Parameters")
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        beta = st.number_input("Infection rate (β)", min_value=0.0, max_value=2.0, value=DEFAULTS["beta"], step=0.01)
    if model_choice == "SEIR":
        with col6:
            sigma = st.number_input("Incubation rate (σ)", min_value=0.0, max_value=2.0, value=DEFAULTS.get("sigma", 0.2), step=0.01)
    else:
        sigma = None
    with col7:
        gamma = st.number_input("Recovery rate (γ)", min_value=0.0, max_value=2.0, value=DEFAULTS["gamma"], step=0.01)
    with col8:
        days = st.number_input("Simulation days", min_value=1, max_value=1000, value=DEFAULTS["days"])

    params = dict(
        N=int(N), I0=int(I0), R0=int(R0), days=int(days),
        beta=float(beta), gamma=float(gamma), dt=DEFAULTS["dt"]
    )
    if model_choice == "SEIR":
        params["E0"] = int(E0)
        params["sigma"] = float(sigma)

### --- Parameter Validation ---
if params:
    try:
        if model_choice == "SIR":
            validate_parameters(
                N=params["N"], I0=params["I0"], R0=params["R0"],
                beta=params["beta"], gamma=params["gamma"],
                days=params["days"], dt=params["dt"]
            )
        elif model_choice == "SEIR":
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
                # Prepare DataFrame for download
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
